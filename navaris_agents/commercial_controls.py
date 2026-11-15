"""Fail-closed commercial controls.

Completeness checks are not bank authentication. Cash recognition requires a
trusted bank/finance verifier supplied by the host application and an
independent human approval attestation. No verifier is configured by default.
"""
from __future__ import annotations

from datetime import datetime
from typing import Any, Callable


def _valid_aware_timestamp(value: Any) -> bool:
    try:
        parsed = datetime.fromisoformat(str(value).replace("Z", "+00:00"))
        return parsed.tzinfo is not None and parsed.utcoffset() is not None
    except (TypeError, ValueError):
        return False


def verify_bank_receipt(
    record: dict[str, Any],
    *,
    trusted_verifier: Callable[[dict[str, Any]], dict[str, Any]] | None = None,
) -> dict[str, Any]:
    """Recognize cash only after trusted bank verification, reconciliation and approval.

    A reference, screenshot, metadata fields, or self-asserted boolean cannot
    authenticate a bank credit. Without a trusted verifier this returns zero.
    The host must implement trusted_verifier using an authorized bank/finance
    process and protect the approval identity and audit trail.
    """
    record = record or {}
    required = (
        "opportunity_id", "amount", "currency", "received_date",
        "evidence_type", "evidence_reference_redacted",
    )
    missing = [key for key in required if record.get(key) in (None, "")]
    try:
        amount = float(record.get("amount", 0))
        if amount <= 0:
            missing.append("amount_must_be_positive")
    except (TypeError, ValueError):
        amount = 0.0
        missing.append("amount_must_be_numeric")

    if str(record.get("evidence_type", "")).upper() != "BANK_RECEIPT":
        missing.append("evidence_type_must_be_BANK_RECEIPT")
    if record.get("received_date") and not _valid_aware_timestamp(record["received_date"]):
        missing.append("received_date_must_be_timezone_aware_ISO8601")
    if missing:
        return {
            "status": "UNVERIFIED",
            "cash_collected": 0.0,
            "missing_or_invalid": sorted(set(missing)),
        }

    if trusted_verifier is None:
        return {
            "status": "PENDING_INDEPENDENT_VERIFICATION",
            "cash_collected": 0.0,
            "reason": "No trusted bank/finance verification adapter is configured.",
        }

    try:
        attestation = trusted_verifier(record)
    except Exception:
        return {
            "status": "VERIFICATION_ERROR",
            "cash_collected": 0.0,
            "reason": "Trusted verifier failed; manual review required.",
        }

    attestation = attestation if isinstance(attestation, dict) else {}
    attestation_required = (
        "bank_credit_verified", "reconciled", "human_approved",
        "verified_amount", "verified_currency", "verified_by", "verified_at",
        "approved_by", "approved_at", "reconciliation_reference",
        "bank_transaction_reference",
    )
    absent = [key for key in attestation_required if attestation.get(key) in (None, "")]
    if absent:
        return {
            "status": "PENDING_HUMAN_REVIEW",
            "cash_collected": 0.0,
            "missing_attestation": absent,
        }
    if (
        attestation.get("bank_credit_verified") is not True
        or attestation.get("reconciled") is not True
        or attestation.get("human_approved") is not True
    ):
        return {
            "status": "REJECTED_OR_PENDING",
            "cash_collected": 0.0,
            "reason": "Bank verification, reconciliation and human approval must all pass.",
        }
    try:
        verified_amount = float(attestation["verified_amount"])
    except (TypeError, ValueError):
        verified_amount = 0.0
    if verified_amount != amount:
        return {
            "status": "REJECTED",
            "cash_collected": 0.0,
            "reason": "Verified amount does not match the submitted receipt amount.",
        }
    if str(attestation["verified_currency"]).upper() != str(record["currency"]).upper():
        return {
            "status": "REJECTED",
            "cash_collected": 0.0,
            "reason": "Verified currency does not match the submitted receipt currency.",
        }
    if not _valid_aware_timestamp(attestation["verified_at"]) or not _valid_aware_timestamp(attestation["approved_at"]):
        return {
            "status": "REJECTED",
            "cash_collected": 0.0,
            "reason": "Verification and approval timestamps must be timezone-aware.",
        }

    return {
        "status": "APPROVED",
        "cash_collected": round(verified_amount, 2),
        "opportunity_id": str(record["opportunity_id"]),
        "currency": str(record["currency"]).upper(),
        "evidence_reference_redacted": str(record["evidence_reference_redacted"]),
        "bank_transaction_reference": str(attestation["bank_transaction_reference"]),
        "verified_by": str(attestation["verified_by"]),
        "verified_at": str(attestation["verified_at"]),
        "approved_by": str(attestation["approved_by"]),
        "approved_at": str(attestation["approved_at"]),
        "reconciliation_reference": str(attestation["reconciliation_reference"]),
    }


def verify_demand_supply_match(demand: dict[str, Any], supply: dict[str, Any]) -> dict[str, Any]:
    """Return a human-review candidate only; never authorize commercial action."""
    demand = demand or {}
    supply = supply or {}
    demand_gates = ("buyer_identity_verified", "buyer_authority_verified",
                    "live_demand_verified", "specification_verified",
                    "destination_verified", "need_by_verified")
    supply_gates = ("supplier_identity_verified", "eligibility_verified",
                    "capacity_verified", "availability_verified",
                    "quote_valid_verified", "terms_verified", "documents_verified")
    missing = [f"demand.{k}" for k in demand_gates if demand.get(k) is not True]
    missing += [f"supply.{k}" for k in supply_gates if supply.get(k) is not True]
    for side_name, side in (("demand", demand), ("supply", supply)):
        if not side.get("evidence_reference"):
            missing.append(f"{side_name}.evidence_reference")
    for field in ("specification_key", "destination_key", "currency"):
        left, right = demand.get(field), supply.get(field)
        if not left or not right:
            missing.append(field)
        elif str(left).strip().casefold() != str(right).strip().casefold():
            return {"status": "NO_MATCH", "actionable": False,
                    "reason": f"{field}_mismatch"}
    try:
        requested = float(demand.get("quantity", 0))
        available = float(supply.get("available_quantity", 0))
        if requested <= 0 or available < requested:
            return {"status": "NO_MATCH", "actionable": False,
                    "reason": "insufficient_or_invalid_quantity"}
    except (TypeError, ValueError):
        missing.append("valid_quantity_and_available_quantity")
    if missing:
        return {"status": "HOLD_UNVERIFIED", "actionable": False,
                "missing_evidence": sorted(set(missing))}
    return {
        "status": "MATCHED_FOR_HUMAN_REVIEW",
        "actionable": False,
        "quantity_matched": requested,
        "currency": str(demand["currency"]).upper(),
        "demand_evidence": demand["evidence_reference"],
        "supply_evidence": supply["evidence_reference"],
        "next_step": "Authorized human reviewer must verify evidence and approve any external action.",
    }


def evaluate_sla(record: dict[str, Any]) -> dict[str, Any]:
    """Evaluate a pre-agreed SLA only from timezone-aware timestamps and evidence."""
    required = ("start_at", "stop_at", "target_minutes", "evidence_reference")
    missing = [key for key in required if record.get(key) in (None, "")]
    if record.get("eligible") is not True:
        missing.append("eligible_must_be_true")
    if missing:
        return {"status": "UNVERIFIED", "missing_evidence": sorted(set(missing))}
    try:
        start = datetime.fromisoformat(str(record["start_at"]).replace("Z", "+00:00"))
        stop = datetime.fromisoformat(str(record["stop_at"]).replace("Z", "+00:00"))
        if start.tzinfo is None or stop.tzinfo is None:
            raise ValueError("timezone required")
        target = float(record["target_minutes"])
        paused = float(record.get("paused_minutes", 0))
        elapsed = (stop - start).total_seconds() / 60 - paused
        if target <= 0 or paused < 0 or elapsed < 0:
            raise ValueError("invalid SLA duration")
    except (TypeError, ValueError):
        return {"status": "UNVERIFIED", "missing_evidence": ["valid_timezone_aware_timestamps_and_duration"]}
    return {"status": "SLA_MET" if elapsed <= target else "SLA_BREACHED",
            "elapsed_minutes": round(elapsed, 2), "target_minutes": target,
            "evidence_reference": str(record["evidence_reference"])}
