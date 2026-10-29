"""NAVARIS Core Engine: deterministic formulas and evidence-gated operating registry."""
from __future__ import annotations
from typing import Any

CORE_VERSION = "1.0.0"
CASH_POLICY = "CASH COLLECTED = 0 until a bank receipt is independently verified and reconciled."
DEFAULT_INTERMEDIARY_COMMISSION_RATE = 0.15  # Planning default only; written agreement required.

VERTICALS = (
 {"id":"consulting","name":"Consulting","scope":"Strategy, diagnosis, turnaround and operating-model improvement."},
 {"id":"audit","name":"Audit","scope":"Evidence-based operational, financial and control reviews; no statutory authority implied."},
 {"id":"training","name":"Training","scope":"Corporate training, course design and capability development."},
 {"id":"fund","name":"Fund","scope":"Fund research and investor intelligence; no regulated fund-management claim."},
 {"id":"shipping_agent","name":"Shipping Agent","scope":"Agency coordination only with proper authority and evidenced appointment."},
 {"id":"commercial_rep","name":"Commercial Representation","scope":"OEM/supplier market entry and buyer development under written mandate."},
 {"id":"nvocc","name":"NVOCC","scope":"Applicable registration, authority and operating capability must be verified first."},
 {"id":"iso","name":"ISO / QMS","scope":"QMS implementation/audit support; certification only by an authorized certification body."},
 {"id":"tourism","name":"Tourism","scope":"Tourism and hospitality services subject to applicable licensing."},
)
AUTONOMOUS_AGENTS = (
 {"id":"agent_01","name":"Research & Market Intelligence","purpose":"Find source-backed demand, buyers, tenders, suppliers and market signals."},
 {"id":"agent_02","name":"Business Diagnosis & Strategy","purpose":"Analyze business models, operating constraints, turnaround and value creation."},
 {"id":"agent_03","name":"Finance & Cash Integrity","purpose":"Calculate financial KPIs; separate forecast, invoice, receivable and verified cash."},
 {"id":"agent_04","name":"Commercial & Deal Qualification","purpose":"Qualify buyer need, decision route, supplier fit, pricing evidence and agreement path."},
 {"id":"agent_05","name":"Delivery, Risk & Quality","purpose":"Track scope, compliance gates, delivery readiness, milestones, evidence and corrective action."},
)

def _ratio_percent(numerator: float, denominator: float) -> float | None:
    if float(denominator) <= 0:
        return None
    return float(numerator) / float(denominator) * 100.0

def operating_expense_ratio(opex: float, net_revenue: float) -> float | None:
    """OER = (OPEX / Net Revenue) * 100; None when net revenue <= 0."""
    if float(opex) < 0:
        raise ValueError("OPEX must be non-negative")
    return _ratio_percent(opex, net_revenue)

def operating_margin(ebit: float, net_revenue: float) -> float | None:
    """Operating Margin = (EBIT / Net Revenue) * 100; EBIT may be negative."""
    return _ratio_percent(ebit, net_revenue)

def commission_spread(deal_value: float, rate: float = DEFAULT_INTERMEDIARY_COMMISSION_RATE) -> float:
    """Illustrative intermediary fee; the rate and fee basis require written agreement."""
    value, pct = float(deal_value), float(rate)
    if value < 0:
        raise ValueError("Deal value must be non-negative")
    if not 0 <= pct <= 1:
        raise ValueError("Commission rate must be between 0 and 1")
    return value * pct

def cash_collected(receipt: dict[str, Any] | None) -> float:
    """Fail closed unless a bank receipt has finance verification and reconciliation metadata."""
    if not isinstance(receipt, dict):
        return 0.0
    required = ("amount","currency","bank_transaction_reference","received_date",
                "evidence_reference","verified_by","verified_at","reconciliation_reference")
    if any(not receipt.get(k) for k in required):
        return 0.0
    if receipt.get("evidence_type") != "BANK_RECEIPT":
        return 0.0
    if receipt.get("verification_status") != "VERIFIED_BY_FINANCE":
        return 0.0
    if receipt.get("reconciliation_status") != "RECONCILED":
        return 0.0
    try:
        amount = float(receipt["amount"])
    except (TypeError, ValueError):
        return 0.0
    return amount if amount > 0 else 0.0

def financial_snapshot(*, opex: float, ebit: float, net_revenue: float,
                       receipt: dict[str, Any] | None = None) -> dict[str, Any]:
    return {
        "core_version": CORE_VERSION,
        "operating_expense_ratio_percent": operating_expense_ratio(opex, net_revenue),
        "operating_margin_percent": operating_margin(ebit, net_revenue),
        "cash_collected": cash_collected(receipt),
        "cash_policy": CASH_POLICY,
        "commission_rate_default": DEFAULT_INTERMEDIARY_COMMISSION_RATE,
        "commission_rate_note": "Planning default only; written agreement required.",
    }

def master_registry() -> dict[str, Any]:
    return {
        "system": "NAVARIS Core Engine",
        "version": CORE_VERSION,
        "operating_doctrine": "TARGET → QUALIFY → STRUCTURE → EXECUTE → COLLECT → REPEAT",
        "primary_kpi": "CASH COLLECTED",
        "cash_policy": CASH_POLICY,
        "formulas": {
            "operating_expense_ratio": "OER = (OPEX / Net Revenue) * 100",
            "operating_margin": "Operating Margin = (EBIT / Net Revenue) * 100",
            "commission_spread": "Illustrative fee = Deal Value * 0.15; written agreement required",
        },
        "verticals": list(VERTICALS),
        "autonomous_agents": list(AUTONOMOUS_AGENTS),
        "evidence_chain": ["FACT","SOURCE","FORMULA","CALCULATION","ASSUMPTION","INTERPRETATION","ACTION"],
        "safety_gates": [
            "Unknown is not zero and is not approval.",
            "Cash is zero until a bank receipt is independently verified and reconciled.",
            "Never invent rates, licences, mandates, contracts, purchase intent or collected cash.",
            "External communication, tender submission, binding quotes and financial commitments require human approval.",
            "Regulated services require applicable authority, licence and appointment evidence.",
        ],
    }

if __name__ == "__main__":
    import json
    print(json.dumps(master_registry(), ensure_ascii=False, indent=2))
