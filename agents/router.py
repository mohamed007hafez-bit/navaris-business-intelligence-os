"""Deterministic NAVARIS router with explicit evidence-gated operations."""
import json
import sys

from .shipping import analyze_shipping
from .oilfield import qualify_oilfield
from .financial import analyze_financial
from .controls import activate_sla, classify_cash_status, verify_demand_supply_match
from .database import save_run

ROUTES = {
    "shipping": analyze_shipping,
    "oilfield": qualify_oilfield,
    "financial": analyze_financial,
}

def _run_control(operation, payload):
    if operation == "record_cash":
        return classify_cash_status(payload)
    if operation == "verify_match":
        demand = payload.get("demand", {})
        supply = payload.get("supply", {})
        if not isinstance(demand, dict) or not isinstance(supply, dict):
            raise TypeError("demand and supply must be JSON objects")
        return verify_demand_supply_match(demand, supply)
    if operation == "activate_sla":
        return activate_sla(payload)
    raise ValueError("operation must be one of: record_cash, verify_match, activate_sla")

def route_request(request, persist=True):
    if not isinstance(request, dict):
        raise TypeError("request must be a JSON object")
    payload = request.get("payload", {})
    if not isinstance(payload, dict):
        raise TypeError("payload must be a JSON object")

    operation = str(request.get("operation", "")).strip().lower()
    if operation:
        result = _run_control(operation, payload)
        if persist:
            save_run("control:" + operation, json.dumps(payload, ensure_ascii=False), json.dumps(result, ensure_ascii=False))
        return result

    agent = str(request.get("agent", "")).strip().lower()
    if agent not in ROUTES:
        raise ValueError("agent must be one of: shipping, oilfield, financial; or use a supported control operation")
    result = ROUTES[agent](payload)
    if persist:
        save_run(agent, json.dumps(payload, ensure_ascii=False), json.dumps(result, ensure_ascii=False))
    return result

def main():
    try:
        print(json.dumps(route_request(json.loads(sys.stdin.read() or "{}")), ensure_ascii=False, indent=2))
    except Exception as exc:
        print(json.dumps({"status": "error", "error": str(exc)}, ensure_ascii=False))
        raise SystemExit(1)

if __name__ == "__main__":
    main()
