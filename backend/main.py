"""NAVARIS local coordination API. Deterministic, evidence-gated, no client-money handling."""
from __future__ import annotations
from datetime import datetime, timezone
from typing import Any
from fastapi import FastAPI
from pydantic import BaseModel, Field

app = FastAPI(title="NAVARIS OS Local API", version="2.0.0")

SERVICES = [
 {"id":"well_intervention_coordination","name":"Well Intervention Coordination","scope":"Slickline / Wireline coordination, supervision, QC, documentation and close-out; execution by qualified licensed partner.","fee":"10-15% INDICATIVE ONLY","status":"ACTIVE"},
 {"id":"quality_documentation","name":"Quality Documentation","scope":"ISO 9001:2015-aligned SOPs, checklists, NCR and readiness support; NOT ISO certification.","fee":"USD 500-1500 INDICATIVE ONLY","status":"ACTIVE"},
 {"id":"logistics_coordination","name":"Logistics Coordination","scope":"Spare-parts RFQ, comparison and follow-up; Oman Gateway alternative option, not a guarantee or safe-route claim.","fee":"10-15% INDICATIVE ONLY","status":"ACTIVE"},
 {"id":"marine_coordination","name":"Marine Coordination","scope":"Bunkering, ship-agency, spare-parts supply and offshore-support coordination only; execution by licensed partner.","fee":"NOT SET","status":"PAUSED UNTIL FIRST 3 SERVICE-1 CONTRACTS"},
]
CHARTER = {
 "identity":"KHALIFAROCK",
 "principal":"Dr. Mohamed Hafez Khalifa, DBA",
 "role":"Founder KHALIFAROCK — Entrepreneurial Coordinator",
 "product":"NAVARIS OS — Human + Autonomous Agents",
 "purpose":"Analyzes, coordinates and manages the founder's work tools.",
 "exclusions":["Not a company","Not an asset manager","Not an investment manager","Not a fund manager","Not an NVOCC","Not a shipping agent executor","Not a holder of client money, portfolios or trades"],
 "services":SERVICES,
 "paused":["Fund","NVOCC","Tourism","Shipping Agent as executor","Commercial Representation as a separate vertical"],
 "cash_collected":0,
 "cash_policy":"CASH COLLECTED = 0 until finance verifies and reconciles a CIB USD bank receipt.",
}
class Payload(BaseModel):
    data: dict[str, Any] = Field(default_factory=dict)
    source_refs: list[str] = Field(default_factory=list)
    notes: str = ""

def envelope(name: str, data: dict[str, Any]) -> dict[str, Any]:
    return {"status":"PRELIMINARY","service":"NAVARIS OS","operation":name,"generated_at":datetime.now(timezone.utc).isoformat(),"evidence_status":"REQUIRES EVIDENCE","data":data,"cash_collected":0,"approval_required":True}

@app.get("/health")
def health():
    return {"status":"ok","service":"NAVARIS OS Local API","version":"2.0.0","timestamp":datetime.now(timezone.utc).isoformat()}

@app.get("/discovery")
def discovery():
    return envelope("discovery", {"services":SERVICES,"paused_services":CHARTER["paused"],"cash_collected":0})

@app.get("/charter")
def charter():
    return envelope("charter", CHARTER)

@app.post("/proposal")
def proposal(p: Payload):
    return envelope("proposal", {"request":p.data,"source_refs":p.source_refs,"draft":"DRAFT ONLY — scope, partner qualification, written terms and approval required.","commercial_terms":"Not set; indicative fees are not binding."})

@app.post("/iso-gap")
def iso_gap(p: Payload):
    score=p.data.get("score"); maximum=p.data.get("max_score")
    if isinstance(score,(int,float)) and isinstance(maximum,(int,float)) and maximum>0:
        pct=score/maximum*100
        return envelope("iso-gap", {"iso_percent":pct,"gap_percent":100-pct,"basis":"ISO% = Score / Max * 100; Gap% = 100 - ISO%","scope":"Quality documentation only; NOT ISO certification."})
    return envelope("iso-gap", {"iso_percent":None,"gap_percent":None,"result":"No data - Requires Evidence"})

@app.post("/risk")
def risk(p: Payload):
    likelihood=p.data.get("likelihood"); impact=p.data.get("impact")
    result=likelihood*impact if isinstance(likelihood,(int,float)) and isinstance(impact,(int,float)) else None
    return envelope("risk", {"risk_score":result,"formula":"Risk = L x I","result":"Calculated" if result is not None else "No data - Requires Evidence"})

@app.post("/daily")
def daily(p: Payload):
    return envelope("daily", {"tasks":p.data.get("tasks",[]),"cash_collected":0,"rule":"No receipt = zero recognized cash."})

@app.post("/closeout")
def closeout(p: Payload):
    required=["scope","partner_qualification","supervision_record","qc_record","document_pack","client_acceptance"]
    supplied=p.data
    missing=[k for k in required if not supplied.get(k)]
    return envelope("closeout", {"required_evidence":required,"missing":missing,"closeout_status":"BLOCKED" if missing else "DRAFT — HUMAN REVIEW REQUIRED","execution_by":"Qualified licensed partner"})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.main:app", host="127.0.0.1", port=8000, reload=False)
