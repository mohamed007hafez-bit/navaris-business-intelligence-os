"""NAVARIS ROOT identity and authorization primitives.

The configured owner email identifies the logical ROOT account. This is an
application-level role check, not cryptographic proof of identity; production
deployment should add device-bound credentials and OS account verification.
"""
from __future__ import annotations

import os
from dataclasses import dataclass
from enum import Enum
from pathlib import PurePosixPath

ROOT_EMAIL = "mohamed007hafez@gmail.com"
ROOT_HANDLE = "mohamed007hafez-bit"
ROOT_ROLE = "ROOT"
BRANCH_ROLE = "BRANCH"

# Paths reserved to the origin device. Branches cannot write these paths via
# the application API; repository protections must additionally enforce this.
ROOT_PROTECTED_PATHS = (
    "src/core/root.py",
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
    email: str
    role: NodeRole
    node_id: str


def normalize_email(email: str | None) -> str:
    return (email or "").strip().casefold()


def identify_node(email: str | None, node_id: str | None = None) -> NodeIdentity:
    normalized = normalize_email(email)
    if not normalized:
        raise ValueError("A configured account email is required.")
    role = NodeRole.ROOT if normalized == ROOT_EMAIL.casefold() else NodeRole.BRANCH
    return NodeIdentity(email=normalized, role=role, node_id=node_id or ROOT_HANDLE)


def is_root(email: str | None) -> bool:
    return normalize_email(email) == ROOT_EMAIL.casefold()


def can_write_path(role: NodeRole | str, path: str) -> bool:
    """Return False when a BRANCH attempts to mutate ROOT-owned files."""
    role_value = role.value if isinstance(role, NodeRole) else str(role).upper()
    if role_value == ROOT_ROLE:
        return True
    normalized = str(PurePosixPath(path)).lstrip("./")
    for protected in ROOT_PROTECTED_PATHS:
        if protected.endswith("/"):
            if normalized.startswith(protected):
                return False
        elif normalized == protected:
            return False
    return True


def configured_identity() -> NodeIdentity:
    """Load the local account identity; never silently promote an unknown user."""
    email = os.environ.get("NAVARIS_OWNER_EMAIL", "")
    node_id = os.environ.get("NAVARIS_NODE_ID", "local-branch")
    return identify_node(email, node_id)
