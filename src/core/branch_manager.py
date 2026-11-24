"""Branch decision interface. Raw ROOT data is never exposed here."""
from __future__ import annotations

from enum import Enum


class Decision(str, Enum):
    GREEN = "🟢"
    AMBER = "🟡"
    RED = "🔴"


def get_decision(status: str | Decision = Decision.AMBER) -> str:
    """Return only a traffic-light decision; never return source records or metrics."""
    if isinstance(status, Decision):
        return status.value
    normalized = str(status).strip().lower()
    mapping = {
        "green": Decision.GREEN.value, "🟢": Decision.GREEN.value,
        "amber": Decision.AMBER.value, "yellow": Decision.AMBER.value, "🟡": Decision.AMBER.value,
        "red": Decision.RED.value, "🔴": Decision.RED.value,
    }
    return mapping.get(normalized, Decision.AMBER.value)
