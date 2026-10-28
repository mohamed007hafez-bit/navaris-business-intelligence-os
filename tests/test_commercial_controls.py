from navaris_agents.commercial_controls import evaluate_sla, verify_bank_receipt, verify_demand_supply_match
from navaris_agents.router import route_request
import pytest

def valid_receipt():
    return {"opportunity_id":"NAV-OPP-001","amount":125,"currency":"EGP",
            "received_date":"2026-10-27T10:00:00+03:00","evidence_type":"BANK_RECEIPT",
            "evidence_reference_redacted":"RCPT-001-REDACTED","verified_by":"reviewer-id",
            "verified_at":"2026-10-27T10:05:00+03:00"}

def valid_demand():
    return {"buyer_identity_verified":True,"buyer_authority_verified":True,"live_demand_verified":True,
            "specification_verified":True,"destination_verified":True,"need_by_verified":True,
            "specification_key":"PCE-VALVE-1","destination_key":"ALEXANDRIA","currency":"USD",
            "quantity":2,"evidence_reference":"RFQ-REDACTED-1"}

def valid_supply():
    return {"supplier_identity_verified":True,"eligibility_verified":True,"capacity_verified":True,
            "availability_verified":True,"quote_valid_verified":True,"terms_verified":True,
            "documents_verified":True,"specification_key":"PCE-VALVE-1","destination_key":"ALEXANDRIA",
            "currency":"USD","available_quantity":3,"evidence_reference":"QUOTE-REDACTED-1"}

def test_boolean_receipt_flag_is_not_enough():
    result=verify_bank_receipt({"receipt_verified":True,"amount":500})
    assert result["status"]=="UNVERIFIED" and result["cash_collected"]==0

def test_full_receipt_metadata_verifies():
    result=verify_bank_receipt(valid_receipt())
    assert result["status"]=="RECEIVED_VERIFIED" and result["cash_collected"]==125

def test_demand_supply_match_requires_all_gates():
    assert verify_demand_supply_match(valid_demand(),valid_supply())["status"]=="MATCH_VERIFIED"
    weak=valid_supply(); weak["capacity_verified"]=False
    assert verify_demand_supply_match(valid_demand(),weak)["status"]=="HOLD_UNVERIFIED"

def test_spec_mismatch_is_not_match():
    supply=valid_supply(); supply["specification_key"]="OTHER"
    assert verify_demand_supply_match(valid_demand(),supply)["status"]=="NO_MATCH"

def test_sla_requires_timezone_and_evidence():
    weak=evaluate_sla({"start_at":"2026-10-27T10:00:00","stop_at":"2026-10-27T10:30:00",
                       "target_minutes":60,"eligible":True,"evidence_reference":"LOG-1"})
    assert weak["status"]=="UNVERIFIED"
    good=evaluate_sla({"start_at":"2026-10-27T10:00:00+03:00","stop_at":"2026-10-27T10:30:00+03:00",
                       "target_minutes":60,"eligible":True,"evidence_reference":"LOG-2"})
    assert good["status"]=="SLA_MET"

def test_commercial_routes_are_disabled_by_default():
    with pytest.raises(PermissionError):
        route_request("commercial","receipt_verify",valid_receipt())
