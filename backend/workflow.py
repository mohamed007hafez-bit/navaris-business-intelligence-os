"""Deterministic, user-triggered NAVARIS workflow agents.

These agents organize supplied information; they do not browse, infer missing facts,
make business commitments, or communicate externally.
"""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

AGENT_SEQUENCE = (
    "intake",
    "evidence_validation",
    "risk_review",
    "strategy_planning",
    "quality_review",
)


def run_workflow(payload: dict[str, Any]) -> dict[str, Any]:
    """Run the deterministic local workflow on explicitly supplied case data."""
    case = payload if isinstance(payload, dict) else {}
    facts = case.get("facts", [])
    risks = case.get("risks", [])
    if not isinstance(facts, list):
        facts = []
    if not isinstance(risks, list):
        risks = []

    missing: list[str] = []
    normalized_facts: list[dict[str, Any]] = []
    for index, fact in enumerate(facts, start=1):
        if not isinstance(fact, dict):
            missing.append(f"FACT-{index:03d}: fact must be an object")
            continue
        label = str(fact.get("label", "")).strip() or f"FACT-{index:03d}"
        source_ref = str(fact.get("source_ref", "")).strip()
        if fact.get("value") is None or fact.get("value") == "":
            missing.append(f"{label}: value is missing")
        if not source_ref:
            missing.append(f"{label}: source reference is missing")
        normalized_facts.append({
            "label": label,
            "value": fact.get("value"),
            "unit": fact.get("unit"),
            "source_ref": source_ref or None,
            "status": "EVIDENCE_REQUIRED" if not source_ref else "SOURCE_PROVIDED_NOT_VERIFIED",
        })

    risk_results: list[dict[str, Any]] = []
    for index, risk in enumerate(risks, start=1):
        if not isinstance(risk, dict):
            risk_results.append({"id": f"R-{index:03d}", "status": "INVALID_INPUT"})
            continue
        likelihood = risk.get("likelihood")
        impact = risk.get("impact")
        valid = (
            isinstance(likelihood, int) and not isinstance(likelihood, bool)
            and isinstance(impact, int) and not isinstance(impact, bool)
            and 1 <= likelihood <= 5 and 1 <= impact <= 5
        )
        risk_results.append({
            "id": str(risk.get("id", f"R-{index:03d}")),
            "description": str(risk.get("description", "")),
            "score": likelihood * impact if valid else None,
            "formula": "likelihood × impact (each 1–5)",
            "status": "CALCULATED_FROM_INPUT" if valid else "INPUT_REQUIRED",
        })

    required = ("sector", "problem")
    missing_case_fields = [field for field in required if not str(case.get(field, "")).strip()]
    missing.extend(f"Case field required: {field}" for field in missing_case_fields)

    return {
        "workflow_id": f"NAV-{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%fZ')}",
        "status": "DRAFT_REVIEW_REQUIRED",
        "execution_mode": "LOCAL_DETERMINISTIC_USER_TRIGGERED",
        "external_actions": "DISABLED",
        "human_approval_required": True,
        "case": {
            "sector": case.get("sector"),
            "problem": case.get("problem"),
            "facts": normalized_facts,
        },
        "agents": [
            {"agent": "intake", "status": "COMPLETED", "result": "Structured supplied case fields; no facts inferred."},
            {"agent": "evidence_validation", "status": "COMPLETED", "result": "Checked supplied facts for values and source references."},
            {"agent": "risk_review", "status": "COMPLETED", "result": "Calculated only risk scores with valid 1–5 inputs."},
            {"agent": "strategy_planning", "status": "COMPLETED", "result": "Prepared next-step prompts from missing inputs; no recommendations invented."},
            {"agent": "quality_review", "status": "COMPLETED", "result": "Flagged evidence and required-field gaps."},
        ],
        "risk_register": risk_results,
        "evidence_gaps": missing,
        "next_steps": (["Provide missing case fields and source references, then run review again."] if missing else ["Founder review is required before any client-facing use."]),
        "limitations": [
            "No external research, AI model call, file extraction, database persistence, or outbound message was performed.",
            "A supplied source reference is recorded but not independently verified.",
            "Missing financial data is not estimated; no valuation or cash result is produced.",
        ],
    }
