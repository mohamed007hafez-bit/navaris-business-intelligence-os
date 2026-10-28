"""Evidence gates for NAVARIS operations.

These functions validate record completeness and declared status; they cannot
authenticate a bank document or independently verify counterparties. CASH_COLLECTED
requires an explicit reconciliation record from an authorized finance reviewer.
"""
from decimal import Decimal, InvalidOperation


def _nonempty(record, keys):
    return [key for key in keys if not str(record.get(key, "")).strip()]


def classify_cash_status(record):
    """Classify cash only after bank-credit evidence is marked reconciled."""
    record = record or {}
    required = (
        "invoice_id", "bank_transaction_reference", "bank_posted_date",
        "payer_legal_name", "expected_payer_legal_name", "amount", "expected_amount", "currency", "expected_currency", "evidence_sha256",
        "finance_reviewer_id", "verified_at", "verification_status",
        "reconciliation_reference", "reconciliation_status",
    )
    missing = _nonempty(record, required)
    if missing:
        return {"status": "PAYMENT_PENDING", "missing_evidence": missing}
    try:
        amount = Decimal(str(record["amount"]))
    except (InvalidOperation, ValueError, TypeError):
        return {"status": "PAYMENT_PENDING", "missing_evidence": ["valid_amount"]}
    if not amount.is_finite() or amount <= 0:
        return {"status": "PAYMENT_PENDING", "missing_evidence": ["positive_amount"]}
    try:
        expected_amount = Decimal(str(record["expected_amount"]))
    except (InvalidOperation, ValueError, TypeError):
        return {"status": "PAYMENT_PENDING", "missing_evidence": ["valid_expected_amount"]}
    if not expected_amount.is_finite() or amount != expected_amount:
        return {"status": "PAYMENT_PENDING", "missing_evidence": ["amount_reconciliation_mismatch"]}
    if str(record["currency"]).upper() != str(record["expected_currency"]).upper():
        return {"status": "PAYMENT_PENDING", "missing_evidence": ["currency_reconciliation_mismatch"]}
    if str(record["payer_legal_name"]).strip().casefold() != str(record["expected_payer_legal_name"]).strip().casefold():
        return {"status": "PAYMENT_PENDING", "missing_evidence": ["payer_reconciliation_mismatch"]}
    if str(record["verification_status"]).upper() != "VERIFIED_BY_FINANCE":
        return {"status": "PAYMENT_PENDING", "missing_evidence": ["finance_verification_status"]}
    if str(record["reconciliation_status"]).upper() != "RECONCILED":
        return {"status": "PAYMENT_PENDING", "missing_evidence": ["bank_reconciliation_status"]}
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
        "reconciliation_reference": str(record["reconciliation_reference"]),
        "note": "Record is marked reconciled; underlying bank evidence and reviewer authority must be authenticated by the operating system or authorized finance process.",
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
