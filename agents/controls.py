"""Evidence gates for NAVARIS operations.

These validators enforce required fields and state transitions; they do NOT
authenticate bank documents, counterparties, signatures, or supplier evidence.
Those facts must be verified by an authorized human or trusted integration.
"""
from decimal import Decimal, InvalidOperation

def _nonempty(record, keys):
    return [key for key in keys if not str(record.get(key, "")).strip()]

def classify_cash_status(record):
    """Return CASH_COLLECTED only for a complete finance-reviewed bank-credit record."""
    required = (
        "invoice_id", "bank_transaction_reference", "bank_posted_date",
        "payer_legal_name", "amount", "currency", "evidence_sha256",
        "finance_reviewer_id", "verified_at", "verification_status",
    )
    missing = _nonempty(record or {}, required)
    if missing:
        return {"status": "PAYMENT_PENDING", "missing_evidence": missing}
    try:
        amount = Decimal(str(record["amount"]))
    except (InvalidOperation, ValueError, TypeError):
        return {"status": "PAYMENT_PENDING", "missing_evidence": ["valid_amount"]}
    if not amount.is_finite() or amount <= 0:
        return {"status": "PAYMENT_PENDING", "missing_evidence": ["positive_amount"]}
    if str(record["verification_status"]).upper() != "VERIFIED_BY_FINANCE":
        return {"status": "PAYMENT_PENDING", "missing_evidence": ["finance_verification_status"]}
    if len(str(record["evidence_sha256"]).strip()) != 64:
        return {"status": "PAYMENT_PENDING", "missing_evidence": ["evidence_sha256_must_be_64_chars"]}
    return {
        "status": "CASH_COLLECTED",
        "invoice_id": str(record["invoice_id"]),
        "amount": str(amount),
        "currency": str(record["currency"]).upper(),
        "bank_transaction_reference": str(record["bank_transaction_reference"]),
        "verified_by": str(record["finance_reviewer_id"]),
        "verified_at": str(record["verified_at"]),
        "note": "Schema-complete only; the evidence and bank posting must be independently authenticated.",
    }

def verify_demand_supply_match(demand, supply):
    """Require independently evidenced buyer demand and supplier capability."""
    demand_required = ("demand_id", "buyer_evidence_ref", "specification", "quantity", "location", "required_date")
    supply_required = ("supplier_id", "supplier_evidence_ref", "specification", "available_quantity", "location", "available_from")
    missing = [f"demand.{k}" for k in _nonempty(demand or {}, demand_required)]
    missing += [f"supply.{k}" for k in _nonempty(supply or {}, supply_required)]
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
    if qty <= 0 or available < qty:
        return {"status": "NO_MATCH", "reason": "insufficient_quantity"}
    return {
        "status": "MATCH_READY_FOR_HUMAN_VERIFICATION",
        "demand_id": str(demand["demand_id"]),
        "supplier_id": str(supply["supplier_id"]),
        "note": "Date, certificates, permits, terms, and evidence authenticity still require review.",
    }

def activate_sla(record):
    """Activate SLA monitoring only after written scope and measurable clock rules exist."""
    required = (
        "signed_scope_ref", "accountable_provider", "availability_evidence_ref",
        "clock_start", "clock_stop", "target_minutes", "timezone",
        "exclusions", "evidence_capture_method", "escalation_owner",
        "acceptance_criteria",
    )
    missing = _nonempty(record or {}, required)
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
        "note": "Readiness gate only; it is not a guarantee that service will be delivered within target.",
    }
