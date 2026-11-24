"""NAVARIS ROOT authority and application-level write controls.

A local environment secret is required in addition to the configured handle.
This is not a substitute for OS account isolation, signed device identity,
GitHub branch protection, or a hardware-backed credential.
"""
from __future__ import annotations

import hmac
import os
from dataclasses import dataclass
from enum import Enum
from pathlib import PurePosixPath

ROOT_HANDLE = "mohamed007hafez-bit"
ROOT_ROLE = "ROOT"
BRANCH_ROLE = "BRANCH"
ROOT_PROTECTED_PATHS = (
    "src/core/root.py",
    "src/core/secure_vault.py",
    "src/core/branch_manager.py",
    "src/core/hybrid_engine.py",
    "main.py",
    "dashboard/app.py",
    ".github/workflows/",
)


class NodeRole(str, Enum):
    ROOT = ROOT_ROLE
    BRANCH = BRANCH_ROLE


@dataclass(frozen=True)
class NodeIdentity:
    handle: str
    role: NodeRole
    node_id: str


class RootAuthority:
    """Promotes only a handle presenting the out-of-band ROOT secret."""
    def __init__(self, root_handle: str = ROOT_HANDLE, root_secret: str | None = None):
        self.root_handle = root_handle.casefold()
        # Expected secret is provisioned out-of-band; caller supplies NAVARIS_ROOT_TOKEN.
        self._root_secret = root_secret if root_secret is not None else os.environ.get("NAVARIS_ROOT_SECRET", "")

    def identify(self, handle: str | None = None, token: str | None = None,
                 node_id: str | None = None) -> NodeIdentity:
        candidate = (handle if handle is not None else os.environ.get("NAVARIS_GITHUB_HANDLE", "")).strip()
        supplied = token if token is not None else os.environ.get("NAVARIS_ROOT_TOKEN", "")
        is_owner = (
            candidate.casefold() == self.root_handle
            and bool(self._root_secret)
            and hmac.compare_digest(supplied.encode(), self._root_secret.encode())
        )
        return NodeIdentity(
            handle=candidate or "unregistered",
            role=NodeRole.ROOT if is_owner else NodeRole.BRANCH,
            node_id=node_id or os.environ.get("NAVARIS_NODE_ID", "local-branch"),
        )

    def is_root(self, identity: NodeIdentity) -> bool:
        return identity.role is NodeRole.ROOT

    def can_write_path(self, identity: NodeIdentity, path: str) -> bool:
        if not self.is_root(identity):
            return False
        normalized = str(PurePosixPath(path)).lstrip("./")
        return not normalized.startswith("../")


def configured_identity() -> NodeIdentity:
    return RootAuthority().identify()
