"""Cloud bridge policy: local-only by default; no token or network call is made here."""
from __future__ import annotations
import os


def should_call_cloud(grade: str, manual_approval: bool = False) -> bool:
    """Cloud is allowed only for an excellent grade + explicit human approval + opt-in.

    This function is a policy gate only. It does not make a network request.
    """
    enabled = os.getenv("NAVARIS_ALLOW_CLOUD", "").strip().lower() in {"1", "true", "yes"}
    return grade == "ممتاز" and manual_approval is True and enabled
