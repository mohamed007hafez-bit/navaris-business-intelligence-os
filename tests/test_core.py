from agents.router import route_request
from agents.shipping import analyze_shipping
from agents.oilfield import qualify_oilfield
from agents.financial import analyze_financial
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
