"""Evidence gates for NAVARIS operations.

These functions validate record completeness and declared status; they cannot
authenticate a bank document or independently verify counterparties. CASH_COLLECTED
requires an explicit reconciliation record from an authorized finance reviewer.
"""
from decimal import Decimal, InvalidOperation


def _nonempty(record, keys):
    return [key for key in keys if not str(record.get(key, "")).strip()]


def classify_cash_status(record, *, trusted_verifier=None):
    """Classify cash only from an independently trusted, approved attestation.

    This module cannot authenticate bank records itself. Without a trusted
    verifier supplied by the host, a claim remains PAYMENT_PENDING.
    """
    record = record or {}
    if trusted_verifier is None:
        return {
            "status": "PAYMENT_PENDING",
            "missing_evidence": ["trusted_bank_finance_verifier_not_configured"],
        }
    try:
        attestation = trusted_verifier(record)
    except Exception:
        return {"status": "PAYMENT_PENDING", "missing_evidence": ["trusted_verifier_error"]}
    if not isinstance(attestation, dict) or attestation.get("status") != "APPROVED":
        return {"status": "PAYMENT_PENDING", "missing_evidence": ["approved_bank_reconciliation_attestation"]}
    required = (
        "invoice_id", "bank_transaction_reference", "bank_posted_date",
        "payer_legal_name", "expected_payer_legal_name", "amount",
        "expected_amount", "currency", "expected_currency", "evidence_sha256",
    )
    missing = _nonempty(record, required)
    try:
        amount = Decimal(str(record["amount"]))
        expected_amount = Decimal(str(record["expected_amount"]))
        attested_amount = Decimal(str(attestation.get("cash_collected", "0")))
    except (InvalidOperation, ValueError, TypeError, KeyError):
        return {"status": "PAYMENT_PENDING", "missing_evidence": ["valid_amounts"]}
    if not amount.is_finite() or amount <= 0 or amount != expected_amount or amount != attested_amount:
        missing.append("amount_reconciliation_mismatch")
    if str(record.get("currency", "")).upper() != str(record.get("expected_currency", "")).upper():
        missing.append("currency_reconciliation_mismatch")
    if str(record.get("payer_legal_name", "")).strip().casefold() != str(record.get("expected_payer_legal_name", "")).strip().casefold():
        missing.append("payer_reconciliation_mismatch")
    if len(str(record.get("evidence_sha256", "")).strip()) != 64:
        missing.append("evidence_sha256_must_be_64_chars")
    for key in ("verified_by", "verified_at", "approved_by", "approved_at", "reconciliation_reference"):
        if not attestation.get(key):
            missing.append(f"attestation_{key}")
    if missing:
        return {"status": "PAYMENT_PENDING", "missing_evidence": sorted(set(missing))}
    return {
        "status": "CASH_COLLECTED",
        "invoice_id": str(record["invoice_id"]),
        "amount": str(amount),
        "currency": str(record["currency"]).upper(),
        "bank_transaction_reference": str(record["bank_transaction_reference"]),
        "verified_by": str(attestation["verified_by"]),
        "verified_at": str(attestation["verified_at"]),
        "approved_by": str(attestation["approved_by"]),
        "approved_at": str(attestation["approved_at"]),
        "reconciliation_reference": str(attestation["reconciliation_reference"]),
        "note": "The trusted verifier attested bank verification, reconciliation and approval; its implementation and reviewer authority must be independently secured.",
    }


def verify_demand_supply_match(demand, supply):
    """Require evidenced demand/supply records; return a review status, never execute."""
    demand = demand or {}
    supply = supply or {}
    demand_required = ("demand_id", "buyer_evidence_ref", "specification", "quantity", "location", "required_date")
    supply_required = ("supplier_id", "supplier_evidence_ref", "specification", "available_quantity", "location", "available_from")
    missing = [f"demand.{k}" for k in _nonempty(demand, demand_required)]
    missing += [f"supply.{k}" for k in _nonempty(supply, supply_required)]
    if missing:
        return {"status": "NEEDS_EVIDENCE", "missing_evidence": missing}
    if str(demand["specification"]).strip().casefold() != str(supply["specification"]).strip().casefold():
        return {"status": "NO_MATCH", "reason": "specification_mismatch"}
    if str(demand["location"]).strip().casefold() != str(supply["location"]).strip().casefold():
        return {"status": "NEEDS_REVIEW", "reason": "location_compatibility_not_proven"}
    try:
        qty = Decimal(str(demand["quantity"]))
        available = Decimal(str(supply["available_quantity"]))
    except (InvalidOperation, ValueError, TypeError):
        return {"status": "NEEDS_EVIDENCE", "missing_evidence": ["valid_quantity_values"]}
    if not qty.is_finite() or not available.is_finite() or qty <= 0 or available < qty:
        return {"status": "NO_MATCH", "reason": "insufficient_or_invalid_quantity"}
    return {
        "status": "MATCH_READY_FOR_HUMAN_VERIFICATION",
        "demand_id": str(demand["demand_id"]),
        "supplier_id": str(supply["supplier_id"]),
        "note": "Date, certificates, permits, commercial terms and evidence authenticity still require review; this is not execution approval.",
    }


def activate_sla(record):
    """Activate SLA monitoring readiness only when written scope and clock rules exist."""
    record = record or {}
    required = (
        "signed_scope_ref", "accountable_provider", "availability_evidence_ref",
        "clock_start", "clock_stop", "target_minutes", "timezone",
        "exclusions", "evidence_capture_method", "escalation_owner",
        "acceptance_criteria",
    )
    missing = _nonempty(record, required)
    if missing:
        return {"status": "SLA_NOT_ACTIVE", "missing_requirements": missing}
    try:
        target = int(record["target_minutes"])
    except (ValueError, TypeError):
        return {"status": "SLA_NOT_ACTIVE", "missing_requirements": ["valid_target_minutes"]}
    if target <= 0:
        return {"status": "SLA_NOT_ACTIVE", "missing_requirements": ["positive_target_minutes"]}
    return {
        "status": "SLA_MONITORING_READY",
        "target_minutes": target,
        "note": "Readiness gate only; not a service guarantee. Activate contractual monitoring only after authorized acceptance is verified.",
    }
