"""NAVARIS encrypted local vault.

SQLCipher encrypts the database; AES-256-GCM encrypts record and file payloads.
The TPM/HSM adapters below are MOCKS, not hardware security modules.
"""
from __future__ import annotations

import hashlib
import hmac
import json
import os
import secrets
import threading
import time
from pathlib import Path
from typing import Any

try:
    from sqlcipher3 import dbapi2 as sqlcipher
except ImportError:
    sqlcipher = None

try:
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM
except ImportError:
    AESGCM = None


class VaultSecurityError(RuntimeError):
    pass


class TPM2Mock:
    """Mock adapter only; no hardware-backed TPM attestation."""
    provider = "TPM 2.0 MOCK"

    def seal(self, key: bytes) -> bytes:
        return key

    def unseal(self, sealed: bytes) -> bytes:
        return sealed


class HSMMock:
    """Mock adapter only; no hardware-backed HSM key custody."""
    provider = "HSM MOCK"

    def sign(self, payload: bytes, key: bytes) -> str:
        return hmac.new(key, payload, hashlib.sha256).hexdigest()


class SecureVault:
    def __init__(self, db_path: str | Path | None = None, key_path: str | Path | None = None):
        if sqlcipher is None:
            raise VaultSecurityError("SQLCipher unavailable; plaintext fallback is disabled.")
        if AESGCM is None:
            raise VaultSecurityError("cryptography unavailable; AES-256-GCM cannot start.")
        data_dir = Path(os.environ.get("NAVARIS_DATA_DIR", Path.home() / ".navaris"))
        data_dir.mkdir(parents=True, exist_ok=True)
        self.db_path = Path(db_path) if db_path else data_dir / "vault.db"
        self.key_path = Path(key_path) if key_path else data_dir / "vault.key"
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._lock = threading.RLock()
        self.tpm, self.hsm = TPM2Mock(), HSMMock()
        self._key = self._load_or_create_key()
        self._aes = AESGCM(self._key)
        self._conn = None
        self.start()

    def _load_or_create_key(self) -> bytes:
        env_key = os.environ.get("NAVARIS_VAULT_KEY")
        if env_key:
            try:
                key = bytes.fromhex(env_key)
            except ValueError as exc:
                raise VaultSecurityError("NAVARIS_VAULT_KEY must be 64 hex characters.") from exc
            if len(key) != 32:
                raise VaultSecurityError("NAVARIS_VAULT_KEY must decode to 32 bytes.")
            return key
        if self.key_path.exists():
            key = self.key_path.read_bytes()
            if len(key) != 32:
                raise VaultSecurityError("Invalid key file; refusing silent key regeneration.")
            return key
        key = secrets.token_bytes(32)
        fd = os.open(str(self.key_path), os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
        with os.fdopen(fd, "wb") as handle:
            handle.write(key)
            handle.flush()
            os.fsync(handle.fileno())
        return key

    @staticmethod
    def is_offline() -> bool:
        """Software configuration check; physical air-gap requires OS/network controls."""
        return os.environ.get("NAVARIS_OFFLINE", "1").strip().lower() in {"1", "true", "yes"}

    def start(self) -> "SecureVault":
        with self._lock:
            if self._conn is not None:
                return self
            self._conn = sqlcipher.connect(str(self.db_path), check_same_thread=False)
            cipher_key = hashlib.sha256(self._key + b"NAVARIS-SQLCIPHER").hexdigest()
            self._conn.execute(f"PRAGMA key = \"x'{cipher_key}'\"")
            version = self._conn.execute("PRAGMA cipher_version").fetchone()
            if not version or not version[0]:
                self._conn.close()
                self._conn = None
                raise VaultSecurityError("SQLCipher cipher_version unavailable; refusing plaintext DB.")
            self._conn.execute("""
                CREATE TABLE IF NOT EXISTS vault_records (
                    record_id TEXT PRIMARY KEY, nonce BLOB NOT NULL,
                    ciphertext BLOB NOT NULL, created_at REAL NOT NULL
                )
            """)
            self._conn.execute("""
                CREATE TABLE IF NOT EXISTS vault_files (
                    file_id TEXT PRIMARY KEY, filename TEXT NOT NULL,
                    content_type TEXT NOT NULL, nonce BLOB NOT NULL,
                    ciphertext BLOB NOT NULL, created_at REAL NOT NULL
                )
            """)
            self._conn.execute("""
                CREATE TABLE IF NOT EXISTS audit_log (
                    seq INTEGER PRIMARY KEY AUTOINCREMENT, created_at REAL NOT NULL,
                    event TEXT NOT NULL, record_id TEXT, previous_hash TEXT NOT NULL,
                    entry_hash TEXT NOT NULL
                )
            """)
            self._conn.execute("""CREATE TRIGGER IF NOT EXISTS audit_no_update
                BEFORE UPDATE ON audit_log BEGIN SELECT RAISE(ABORT, 'append-only audit log'); END""")
            self._conn.execute("""CREATE TRIGGER IF NOT EXISTS audit_no_delete
                BEFORE DELETE ON audit_log BEGIN SELECT RAISE(ABORT, 'append-only audit log'); END""")
            self._conn.commit()
            self._audit("VAULT_STARTED", None)
            return self

    def _require_started(self):
        if self._conn is None:
            raise VaultSecurityError("Vault is not started.")

    def _audit(self, event: str, record_id: str | None) -> None:
        self._require_started()
        row = self._conn.execute("SELECT entry_hash FROM audit_log ORDER BY seq DESC LIMIT 1").fetchone()
        previous = row[0] if row else "0" * 64
        created = time.time()
        body = json.dumps({"created_at": created, "event": event, "record_id": record_id,
                           "previous_hash": previous}, sort_keys=True, separators=(",", ":")).encode()
        digest = hashlib.sha256(body).hexdigest()
        self._conn.execute(
            "INSERT INTO audit_log(created_at,event,record_id,previous_hash,entry_hash) VALUES(?,?,?,?,?)",
            (created, event, record_id, previous, digest))
        self._conn.commit()

    def put_financial_record(self, record_id: str, payload: dict[str, Any]) -> None:
        self._require_started()
        plaintext = json.dumps(payload, ensure_ascii=False, sort_keys=True).encode("utf-8")
        nonce = secrets.token_bytes(12)
        ciphertext = self._aes.encrypt(nonce, plaintext, record_id.encode())
        with self._lock:
            self._conn.execute(
                "INSERT OR REPLACE INTO vault_records VALUES(?,?,?,?)",
                (record_id, nonce, ciphertext, time.time()))
            self._conn.commit()
            self._audit("FINANCIAL_RECORD_STORED_ENCRYPTED", record_id)

    def get_financial_record(self, record_id: str) -> dict[str, Any] | None:
        self._require_started()
        with self._lock:
            row = self._conn.execute(
                "SELECT nonce,ciphertext FROM vault_records WHERE record_id=?", (record_id,)).fetchone()
            if row is None:
                return None
            value = json.loads(self._aes.decrypt(row[0], row[1], record_id.encode()).decode("utf-8"))
            self._audit("FINANCIAL_RECORD_READ", record_id)
            return value

    def encrypt_file(self, file_path: str | Path, file_id: str | None = None,
                     delete_source: bool = True, content_type: str =
                     "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet") -> str:
        """Encrypt a file into the vault_files BLOB table; optionally erase plaintext copy."""
        self._require_started()
        source = Path(file_path)
        if not source.is_file():
            raise FileNotFoundError(source)
        payload = source.read_bytes()
        identifier = file_id or secrets.token_hex(16)
        nonce = secrets.token_bytes(12)
        aad = identifier.encode("utf-8")
        ciphertext = self._aes.encrypt(nonce, payload, aad)
        with self._lock:
            self._conn.execute(
                "INSERT OR REPLACE INTO vault_files(file_id,filename,content_type,nonce,ciphertext,created_at) "
                "VALUES(?,?,?,?,?,?)",
                (identifier, source.name, content_type, nonce, ciphertext, time.time()))
            self._conn.commit()
            self._audit("FILE_ENCRYPTED_IN_VAULT", identifier)
        if delete_source:
            source.unlink()
        return identifier

    def decrypt_file(self, file_id: str, destination: str | Path) -> Path:
        """Explicitly export a decrypted copy; caller controls destination and access."""
        self._require_started()
        row = self._conn.execute(
            "SELECT filename,nonce,ciphertext FROM vault_files WHERE file_id=?", (file_id,)).fetchone()
        if row is None:
            raise KeyError(file_id)
        plaintext = self._aes.decrypt(row[1], row[2], file_id.encode("utf-8"))
        target = Path(destination)
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(plaintext)
        self._audit("FILE_EXPORTED_DECRYPTED", file_id)
        return target

    def verify_audit_chain(self) -> bool:
        self._require_started()
        previous = "0" * 64
        rows = self._conn.execute(
            "SELECT created_at,event,record_id,previous_hash,entry_hash FROM audit_log ORDER BY seq").fetchall()
        for created, event, record_id, stored_previous, stored_hash in rows:
            if stored_previous != previous:
                return False
            body = json.dumps({"created_at": created, "event": event, "record_id": record_id,
                               "previous_hash": previous}, sort_keys=True, separators=(",", ":")).encode()
            if not hmac.compare_digest(hashlib.sha256(body).hexdigest(), stored_hash):
                return False
            previous = stored_hash
        return True

    def close(self) -> None:
        with self._lock:
            if self._conn is not None:
                self._conn.close()
                self._conn = None
