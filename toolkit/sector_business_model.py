"""Evidence-first, cross-sector business model and discovery helper.

This standard-library-only tool creates a discovery worksheet from supplied records.
It does not search the web, invent customers, score investment viability, or contact leads.
"""
from __future__ import annotations

from typing import Any

SECTORS: dict[str, dict[str, Any]] = {
    "consulting_sme": {
        "name": "Business services & SMEs",
        "buyer_segments": ["SME owner / managing director", "functional leader", "family business operator"],
        "discovery_questions": ["Which recurring decision or process is costly or delayed?", "What baseline records demonstrate the issue?", "Who owns the decision and budget?"],
        "boundary": "Use comparable periods and source-backed operating/financial inputs; do not imply audit or investment advice.",
    },
    "energy_oil_gas": {
        "name": "Energy & Oil/Gas",
        "buyer_segments": ["operator procurement / supply chain", "EPC / service contractor", "OEM / technical supplier"],
        "discovery_questions": ["What exact service, equipment specification, site and required date are documented?", "Who has authority to issue the RFQ or approve the supplier?", "Which licenses, HSE controls and qualified execution partners apply?"],
        "boundary": "Technical claims, field execution, supplier authority, HSE, licenses and current requirements require dated evidence and qualified-party review.",
    },
    "maritime_logistics": {
        "name": "Maritime, ports & logistics",
        "buyer_segments": ["shipper / cargo owner", "licensed carrier / forwarder / agent", "port or logistics operator"],
        "discovery_questions": ["What are the origin, destination, cargo, mode, dimensions, weight and dates?", "Are the compared quotes for the same scope, route, Incoterm and validity period?", "Which licensed parties own transport, customs and cargo liability?"],
        "boundary": "Do not represent NAVARIS as carrier, NVOCC, customs broker or shipping agent without verified authority and appointment.",
    },
    "manufacturing": {
        "name": "Manufacturing & industrial",
        "buyer_segments": ["plant manager / operations", "procurement / maintenance", "export or supply-chain manager"],
        "discovery_questions": ["Which line, asset or order is affected, and how is the baseline measured?", "What are the specification, volume, acceptance criteria and delivery window?", "What supplier qualification and quality evidence is required?"],
        "boundary": "Production, quality and saving claims need like-for-like scope, volume, period and source evidence.",
    },
    "construction_infrastructure": {
        "name": "Construction & infrastructure",
        "buyer_segments": ["project owner / developer", "EPC / main contractor", "project controls / procurement"],
        "discovery_questions": ["Which package, milestone, site and contractual scope are involved?", "What schedule, cost or change-control baseline supports the need?", "Who approves variations, vendors and commercial terms?"],
        "boundary": "Do not imply engineering certification, statutory authority or project award; validate contracts and permits with qualified professionals.",
    },
    "aviation_cargo": {
        "name": "Aviation & air cargo",
        "buyer_segments": ["shipper / exporter", "air-cargo handler / forwarder", "airline or airport supplier"],
        "discovery_questions": ["What commodity, dimensions, weight, route and ready date are confirmed?", "What security, dangerous-goods and handling requirements apply?", "Are capacity, quote validity and shipment documents verified?"],
        "boundary": "Aviation, security, dangerous-goods and handling rules must be verified with current authorized sources and operators.",
    },
    "mining_extraction": {
        "name": "Mining & extraction",
        "buyer_segments": ["site operator", "maintenance / procurement", "licensed specialist contractor"],
        "discovery_questions": ["Which site, equipment or service requirement is documented?", "What access, safety, environmental and technical approvals apply?", "Which qualified supplier can meet the specification and schedule?"],
        "boundary": "Site access, safety, environmental, licensing and technical execution require competent authority and evidence.",
    },
    "tourism_hospitality": {
        "name": "Tourism & hospitality",
        "buyer_segments": ["hotel / venue owner", "hospitality operations manager", "corporate travel buyer"],
        "discovery_questions": ["Which property, dates, room/service scope and decision-maker are confirmed?", "Are rates, taxes, availability, cancellation terms and service levels in dated written offers?", "What operational baseline supports the requested improvement?"],
        "boundary": "Property identity, affiliation, rates, availability, licensing and results must be independently checked before publication or commitment.",
    },
    "healthcare": {
        "name": "Healthcare & life sciences",
        "buyer_segments": ["provider administrator", "operations / procurement lead", "licensed healthcare supplier"],
        "discovery_questions": ["What non-clinical operational problem and process are in scope?", "What privacy, safety, procurement and regulatory constraints apply?", "Which approved data and qualified professional are needed?"],
        "boundary": "No clinical advice or patient-sensitive data processing; legal, clinical, privacy and regulatory review are mandatory where relevant.",
    },
    "training_education": {
        "name": "Training & education",
        "buyer_segments": ["HR / L&D leader", "department head", "institution / program owner"],
        "discovery_questions": ["Which role-based skill gap is evidenced?", "What observable workplace behavior or KPI should change?", "Who approves learners, schedule, materials and evaluation?"],
        "boundary": "Do not promise learning ROI without baseline, costs, measurement method and follow-up evidence.",
    },
    "digital_ai": {
        "name": "Digital, data & AI",
        "buyer_segments": ["business process owner", "IT / data leader", "SME owner / digital transformation lead"],
        "discovery_questions": ["Which process, data, system and measurable constraint are in scope?", "What security, privacy, integration, retention and human-review requirements apply?", "What small reversible pilot can validate value and failure modes?"],
        "boundary": "No claims of production AI, security, automation or integrations until implemented and tested; protect credentials and personal data.",
    },
    "public_institution": {
        "name": "Public institutions & NGOs",
        "buyer_segments": ["authorized program owner", "procurement / grants officer", "implementing partner"],
        "discovery_questions": ["What published mandate, program outcome and procurement route apply?", "What eligibility, conflict-of-interest, reporting and data requirements exist?", "Which official notice and deadline establish the opportunity?"],
        "boundary": "Use official notices and procurement rules; no implied government relationship or privileged access.",
    },
}

BMC_BLOCKS = (
    "customer_segments", "problems", "value_propositions", "solutions",
    "channels", "revenue_streams", "cost_structure", "key_metrics", "unfair_advantage",
)
REQUIRED_GATES = {
    "problem_evidence": "A dated record of the customer's problem in their own words or an authorized source.",
    "buyer_route": "A documented, appropriate path to the decision owner; not a guessed contact.",
    "service_fit": "A documented fit between the need and the proposed scope/capability.",
    "delivery_capacity": "Evidence of available internal capacity or a qualified, authorized partner.",
    "commercial_path": "A testable budget/procurement/payment path; not a forecast of revenue.",
}


def _has_source_backed_record(value: Any) -> bool:
    return isinstance(value, dict) and bool(str(value.get("source_ref", "")).strip() and str(value.get("source_date", "")).strip())


def build_business_model(payload: dict[str, Any]) -> dict[str, Any]:
    """Return a framework and evidence gaps; never infer a verified customer or market."""
    if not isinstance(payload, dict):
        raise TypeError("input must be a JSON object")
    sector_id = str(payload.get("sector_id", "")).strip()
    if sector_id not in SECTORS:
        raise ValueError(f"sector_id must be one of: {', '.join(sorted(SECTORS))}")
    sector = SECTORS[sector_id]
    objective = str(payload.get("decision_objective", "")).strip()
    gates = payload.get("gates", {})
    if not isinstance(gates, dict):
        gates = {}
    evidence = payload.get("evidence", [])
    if not isinstance(evidence, list):
        evidence = []
    verified_evidence = [item for item in evidence if _has_source_backed_record(item)]
    missing = [key for key, _description in REQUIRED_GATES.items() if not _has_source_backed_record(gates.get(key))]
    if not objective:
        missing.insert(0, "decision_objective")

    canvas = {key: {"status": "UNKNOWN", "statement": None, "evidence_refs": [], "note": "Enter a testable hypothesis or evidence-backed statement; do not treat a blank as fact."} for key in BMC_BLOCKS}
    segment = str(payload.get("customer_segment", "")).strip() or None
    if segment:
        canvas["customer_segments"].update(status="HYPOTHESIS", statement=segment)

    return {
        "schema_version": "1.0",
        "record_type": "INTERNAL_DISCOVERY_WORKSHEET",
        "status": "READY_FOR_HUMAN_REVIEW" if not missing else "NEEDS_EVIDENCE",
        "evidence_policy": "No external market/client search was run. Company existence or a public directory listing does not establish a current need, buyer authority, budget, or purchase intent.",
        "sector": {"id": sector_id, "name": sector["name"], "boundary": sector["boundary"]},
        "company_name": str(payload.get("company_name", "")).strip() or None,
        "decision_objective": objective or None,
        "customer_segment": segment,
        "candidate_buyer_roles_for_research": list(sector["buyer_segments"]),
        "discovery_questions": list(sector["discovery_questions"]),
        "business_model_canvas": canvas,
        "evidence_records_with_source_and_date": len(verified_evidence),
        "missing_gates": [{"gate": key, "required_evidence": "Define the business decision first." if key == "decision_objective" else REQUIRED_GATES[key]} for key in missing],
        "qualification_rule": "A complete worksheet is only READY_FOR_HUMAN_REVIEW; a person must validate the source, contact route, authority, scope, sector rules and commercial terms before calling a lead qualified.",
        "next_actions": [
            "Choose one specific buyer role and define an interview/discovery question.",
            "Record the official/public source URL, date checked, and evidence status for every claim.",
            "Confirm the problem directly through an authorized, appropriate channel before proposing a solution.",
            "Populate BMC blocks as HYPOTHESIS until a dated source or customer evidence supports them.",
        ],
        "external_contact_sent": False,
        "cash_collected": 0,
    }


def main() -> int:
    import argparse
    import json
    from pathlib import Path
    parser = argparse.ArgumentParser(description="Build a cross-sector NAVARIS discovery/business-model worksheet from supplied evidence.")
    parser.add_argument("--input", type=Path, required=True, help="JSON intake file; no live web search is performed.")
    parser.add_argument("--output", type=Path, help="Optional output JSON path; defaults to stdout.")
    args = parser.parse_args()
    try:
        result = build_business_model(json.loads(args.input.read_text(encoding="utf-8")))
    except (OSError, json.JSONDecodeError, TypeError, ValueError) as exc:
        parser.error(str(exc))
    rendered = json.dumps(result, ensure_ascii=False, indent=2) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered, encoding="utf-8")
    else:
        print(rendered, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
