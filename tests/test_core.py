from agents.router import route_request
from agents.shipping import analyze_shipping
from agents.oilfield import qualify_oilfield
from agents.financial import analyze_financial
from agents.controls import activate_sla, classify_cash_status, verify_demand_supply_match

def test_shipping_missing_rates_not_invented():
 r=analyze_shipping({"freight":100}); assert r["status"]=="needs_inputs" and r["total_landed_cost"] is None
def test_shipping_cost_calculation():
 r=analyze_shipping({"freight":100,"customs":20,"handling":5,"insurance":2}); assert r["total_landed_cost"]=="127"
def test_oilfield_requires_scope():
 r=qualify_oilfield({"client":"Client"}); assert r["status"]=="needs_inputs" and "service_scope" in r["missing_inputs"]
def test_financial_metrics():
 r=analyze_financial({"current_assets":200,"current_liabilities":100,"revenue":500,"ebitda":50,"inventory":20})
 assert r["current_ratio"]=="2.00" and r["working_capital"]=="100" and r["ebitda_margin_percent"]=="10.00"
def test_router_rejects_unknown_agent():
 try: route_request({"agent":"unknown","payload":{}},persist=False)
 except ValueError as e: assert "shipping, oilfield, financial" in str(e)
 else: raise AssertionError("unknown agent must fail")
def test_negative_shipping_cost_rejected():
 try: analyze_shipping({"freight":-1,"customs":0,"handling":0})
 except ValueError: pass
 else: raise AssertionError("negative cost must fail")
def test_cash_not_collected_from_invoice_or_incomplete_proof():
 r=classify_cash_status({"invoice_id":"INV-1","amount":"100","currency":"USD"})
 assert r["status"]=="PAYMENT_PENDING"
def test_cash_requires_finance_verified_bank_evidence():
 r=classify_cash_status({"invoice_id":"INV-1","bank_transaction_reference":"TX-1","bank_posted_date":"2026-10-28","payer_legal_name":"Buyer Ltd","expected_payer_legal_name":"Buyer Ltd","amount":"100","expected_amount":"100","currency":"USD","expected_currency":"USD","evidence_sha256":"a"*64,"finance_reviewer_id":"finance-01","verified_at":"2026-10-28T10:00:00Z","verification_status":"VERIFIED_BY_FINANCE","reconciliation_reference":"REC-1","reconciliation_status":"RECONCILED"})
 assert r["status"]=="CASH_COLLECTED"
def test_cash_rejects_unreviewed_claim():
 r=classify_cash_status({"invoice_id":"INV-1","bank_transaction_reference":"TX-1","bank_posted_date":"2026-10-28","payer_legal_name":"Buyer Ltd","amount":"100","currency":"USD","evidence_sha256":"a"*64,"finance_reviewer_id":"finance-01","verified_at":"2026-10-28T10:00:00Z","verification_status":"SELF_REPORTED","reconciliation_reference":"REC-1","reconciliation_status":"RECONCILED"})
 assert r["status"]=="PAYMENT_PENDING"
def test_match_requires_evidence():
 assert verify_demand_supply_match({}, {})["status"]=="NEEDS_EVIDENCE"
def test_match_rejects_specification_mismatch():
 d={"demand_id":"D1","buyer_evidence_ref":"buyer.pdf","specification":"Valve A","quantity":2,"location":"Alexandria","required_date":"2026-11-05"}
 s={"supplier_id":"S1","supplier_evidence_ref":"quote.pdf","specification":"Valve B","available_quantity":4,"location":"Alexandria","available_from":"2026-11-01"}
 assert verify_demand_supply_match(d,s)["status"]=="NO_MATCH"
def test_sla_not_active_without_signed_scope():
 assert activate_sla({"target_minutes":180})["status"]=="SLA_NOT_ACTIVE"

def test_router_cash_control_requires_reconciliation():
 r=route_request({"operation":"record_cash","payload":{"invoice_id":"INV-2"}},persist=False)
 assert r["status"]=="PAYMENT_PENDING"

def test_router_match_control_is_review_only():
 r=route_request({"operation":"verify_match","payload":{"demand":{},"supply":{}}},persist=False)
 assert r["status"]=="NEEDS_EVIDENCE"

def test_router_sla_control_does_not_assume_three_hour_promise():
 r=route_request({"operation":"activate_sla","payload":{"target_minutes":180}},persist=False)
 assert r["status"]=="SLA_NOT_ACTIVE"
