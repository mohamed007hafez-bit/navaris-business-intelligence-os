"""Offline-first NAVARIS reasoning engine.

OFFLINE is the startup default. Network access is attempted only after the
operator explicitly switches this process to ONLINE. The local SQLite store
records queries and provides a small persistent local knowledge base.
"""
from __future__ import annotations

import json
import os
import sqlite3
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

MODE = "offline"
DEFAULT_MODEL = os.environ.get("OPENAI_MODEL", "gpt-4o-mini")
API_URL = os.environ.get("OPENAI_BASE_URL", "https://api.openai.com/v1/chat/completions")


def _data_dir() -> Path:
    if os.name == "nt":
        base = Path(os.environ.get("LOCALAPPDATA", Path.home()))
    else:
        base = Path(os.environ.get("XDG_DATA_HOME", Path.home() / ".local" / "share"))
    target = base / "NavarisOS"
    target.mkdir(parents=True, exist_ok=True)
    return target


def _db_connect() -> sqlite3.Connection:
    connection = sqlite3.connect(_data_dir() / "navaris_brain.sqlite3")
    connection.execute(
        """CREATE TABLE IF NOT EXISTS interactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            created_at TEXT NOT NULL,
            mode TEXT NOT NULL,
            query TEXT NOT NULL,
            response TEXT NOT NULL
        )"""
    )
    connection.execute(
        """CREATE TABLE IF NOT EXISTS knowledge (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            topic TEXT NOT NULL UNIQUE,
            content TEXT NOT NULL
        )"""
    )
    return connection


def set_mode(mode: str) -> str:
    """Explicitly switch network permission; only 'online' enables API calls."""
    global MODE
    normalized = mode.strip().lower()
    if normalized not in {"offline", "online"}:
        raise ValueError("Mode must be 'offline' or 'online'.")
    MODE = normalized
    return MODE


def get_mode() -> str:
    return MODE


def remember(topic: str, content: str) -> None:
    """Persist a local fact in the SQLite brain."""
    topic = topic.strip()
    if not topic:
        raise ValueError("Knowledge topic cannot be empty.")
    with _db_connect() as db:
        db.execute(
            "INSERT INTO knowledge(topic, content) VALUES(?, ?) "
            "ON CONFLICT(topic) DO UPDATE SET content=excluded.content",
            (topic, content.strip()),
        )


def _log(query: str, response: str, mode: str) -> None:
    with _db_connect() as db:
        db.execute(
            "INSERT INTO interactions(created_at, mode, query, response) VALUES(?, ?, ?, ?)",
            (datetime.now(timezone.utc).isoformat(), mode, query, response),
        )


def offline_brain(query: str) -> str:
    """Answer locally with deterministic rules and SQLite knowledge; no network."""
    text = (query or "").strip()
    if not text:
        return "Enter a request for NAVARIS."
    lowered = text.casefold()
    with _db_connect() as db:
        rows = db.execute(
            "SELECT topic, content FROM knowledge ORDER BY topic"
        ).fetchall()
    matches = [(topic, content) for topic, content in rows
               if topic.casefold() in lowered or lowered in topic.casefold()]
    if matches:
        answer = "\n".join(f"{topic}: {content}" for topic, content in matches)
    elif any(word in lowered for word in ("cash", "revenue", "payment", "تحصيل", "كاش")):
        answer = (
            "NAVARIS CASH CONTROL: CASH COLLECTED remains 0 until a bank receipt "
            "is independently verified and reconciled. Next action: identify the "
            "payer, amount, due date, proof, and accountable owner."
        )
    elif any(word in lowered for word in ("plan", "priority", "task", "خطة", "أولوية")):
        answer = (
            "NAVARIS OFFLINE PLAN: define one measurable outcome, list the next "
            "three actions, assign an owner and deadline, then record evidence "
            "before marking the task complete."
        )
    else:
        answer = (
            "NAVARIS OFFLINE BRAIN: local rules are active and no internet was used. "
            "Break the request into objective, constraints, inputs, next action, "
            "and evidence. Add durable facts with remember(topic, content)."
        )
    _log(text, answer, "offline")
    return answer


def online_brain(query: str) -> str:
    """Call the OpenAI-compatible API only when explicitly switched ONLINE."""
    if MODE != "online":
        raise RuntimeError('Online AI is disabled. Type "Navaris go online" first.')
    api_key = os.environ.get("OPENAI_API_KEY") or os.environ.get("API_KEY")
    if not api_key:
        raise RuntimeError("ONLINE mode selected, but OPENAI_API_KEY/API_KEY is not configured.")
    text = (query or "").strip()
    if not text:
        return "Enter a request for NAVARIS."
    payload: dict[str, Any] = {
        "model": DEFAULT_MODEL,
        "messages": [
            {"role": "system", "content": "You are NAVARIS, an enterprise operations assistant. Be precise; never invent evidence or cash receipts."},
            {"role": "user", "content": text},
        ],
        "temperature": 0.2,
    }
    request = urllib.request.Request(
        API_URL,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=45) as response:
            result = json.loads(response.read().decode("utf-8"))
        answer = result["choices"][0]["message"]["content"].strip()
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")[:1000]
        raise RuntimeError(f"AI API returned HTTP {exc.code}: {detail}") from exc
    except (urllib.error.URLError, TimeoutError) as exc:
        raise RuntimeError(f"AI API connection failed: {exc}") from exc
    except (KeyError, IndexError, TypeError, json.JSONDecodeError) as exc:
        raise RuntimeError("AI API returned an unexpected response.") from exc
    _log(text, answer, "online")
    return answer


def execute(query: str) -> str:
    """Dispatch according to current mode; OFFLINE is always the safe default."""
    return online_brain(query) if MODE == "online" else offline_brain(query)
