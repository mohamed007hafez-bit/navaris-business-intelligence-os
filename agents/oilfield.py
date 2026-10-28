"""Oilfield qualification checklist; no operational guarantee."""
CHECKLIST=["Confirm operator/client and authorized contact","Define well, location, service scope, and required date","Confirm equipment specification and certification requirements","Confirm crew, permits, HSE requirements, and site access","Validate equipment and provider availability","Agree written scope, price, mobilization target, and acceptance criteria"]
def qualify_oilfield(payload):
 payload=payload or {}; fields=("client","location","service_scope","required_date")
 missing=[f for f in fields if not str(payload.get(f,"")).strip()]
 return {"agent":"oilfield","status":"needs_inputs" if missing else "ready_for_human_review","missing_inputs":missing,"checklist":CHECKLIST.copy(),"mobilization":"Not guaranteed; confirm provider readiness, permits, equipment, and written SLA.","note":"Qualification checklist only; not operational approval or service commitment."}
