"""Oilfield/energy tender and project-control helpers. No live tender claims are made."""
from __future__ import annotations

from datetime import date
from typing import Any, Iterable


def assess_tender(*, title: str, source_url: str, deadline: str | None,
                  scope_known: bool, eligibility_known: bool, budget_known: bool,
                  documents_available: bool, source_checked: bool = False) -> dict[str, Any]:
    """Score completeness of evidence, not probability of winning a tender."""
    if not title.strip():
        raise ValueError("title is required")
    if source_url and not source_url.startswith(("https://", "http://")):
        raise ValueError("source_url must be an http(s) URL")
    if deadline:
        try:
            deadline_date = date.fromisoformat(deadline)
        except ValueError as exc:
            raise ValueError("deadline must use YYYY-MM-DD") from exc
        days_remaining = (deadline_date - date.today()).days
    else:
        days_remaining = None
    checks = {
        "official_source_checked": bool(source_checked and source_url),
        "scope_known": scope_known,
        "eligibility_known": eligibility_known,
        "budget_known": budget_known,
        "documents_available": documents_available,
    }
    score = sum(checks.values())
    if days_remaining is not None and days_remaining < 0:
        decision = "EXPIRED"
    elif score == len(checks) and days_remaining != 0:
        decision = "READY_FOR_HUMAN_REVIEW"
    else:
        decision = "HOLD_VERIFY"
    return {
        "title": title.strip(), "source_url": source_url or None, "days_remaining": days_remaining,
        "evidence_score": f"{score}/{len(checks)}", "checks": checks, "decision": decision,
        "disclaimer": "This is a completeness gate, not legal advice, a bid decision, or a verified live opportunity.",
    }


def project_risk_register(items: Iterable[dict[str, Any]]) -> list[dict[str, Any]]:
    """Normalize project risks and calculate a transparent likelihood x impact score (1-5 each)."""
    result = []
    for index, item in enumerate(items, start=1):
        likelihood = item.get("likelihood")
        impact = item.get("impact")
        if not isinstance(likelihood, int) or not 1 <= likelihood <= 5:
            raise ValueError(f"risk {index}: likelihood must be an integer from 1 to 5")
        if not isinstance(impact, int) or not 1 <= impact <= 5:
            raise ValueError(f"risk {index}: impact must be an integer from 1 to 5")
        score = likelihood * impact
        result.append({
            "risk_id": str(item.get("risk_id") or f"R-{index:03d}"),
            "description": str(item.get("description") or "Unspecified risk"),
            "likelihood": likelihood, "impact": impact, "score": score,
            "rating": "HIGH" if score >= 15 else "MEDIUM" if score >= 6 else "LOW",
            "owner": item.get("owner"), "mitigation": item.get("mitigation"),
            "status": item.get("status") or "OPEN",
        })
    return result
