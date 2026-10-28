"""Fail-closed commercial controls: receipt verification, demand-supply matching and SLA evidence."""
from __future__ import annotations

from datetime import datetime
from typing import Any


def verify_bank_receipt(record: dict[str, Any]) -> dict[str, Any]:
    """Return verified only when required audit metadata exists; a boolean flag alone is insufficient."""
    required = ("opportunity_id", "amount", "currency", "received_date",
                "evidence_type", "evidence_reference_redacted", "verified_by", "verified_at")
    missing = [key for key in required if record.get(key) in (None, "")]
    try:
        amount = float(record.get("amount", 0))
        if amount <= 0:
            missing.append("amount_must_be_positive")
    except (TypeError, ValueError):
        missing.append("amount_must_be_numeric")
    if str(record.get("evidence_type", "")).upper() != "BANK_RECEIPT":
        missing.append("evidence_type_must_be_BANK_RECEIPT")
    if missing:
        return {"status": "UNVERIFIED", "cash_collected": 0.0,
                "missing_or_invalid": sorted(set(missing))}
    try:
        verified_at = datetime.fromisoformat(str(record["verified_at"]).replace("Z", "+00:00"))
        received_at = datetime.fromisoformat(str(record["received_date"]).replace("Z", "+00:00"))
        if verified_at.tzinfo is None or received_at.tzinfo is None:
            raise ValueError("timezone required")
    except ValueError:
        return {"status": "UNVERIFIED", "cash_collected": 0.0,
                "missing_or_invalid": ["received_date_and_verified_at_must_be_timezone_aware_ISO8601"]}
    return {"status": "RECEIVED_VERIFIED", "cash_collected": round(amount, 2),
            "opportunity_id": str(record["opportunity_id"]),
            "currency": str(record["currency"]).upper(),
            "evidence_reference_redacted": str(record["evidence_reference_redacted"]),
            "verified_by": str(record["verified_by"])}


def verify_demand_supply_match(demand: dict[str, Any], supply: dict[str, Any]) -> dict[str, Any]:
    """Only return MATCH_VERIFIED when every mandatory demand/supply and evidence gate passes."""
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
    return {"status": "MATCH_VERIFIED", "actionable": True,
            "quantity_matched": requested, "currency": str(demand["currency"]).upper(),
            "demand_evidence": demand["evidence_reference"],
            "supply_evidence": supply["evidence_reference"]}


def evaluate_sla(record: dict[str, Any]) -> dict[str, Any]:
    """Evaluate a pre-agreed SLA only from timezone-aware timestamps and a documented evidence reference."""
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
