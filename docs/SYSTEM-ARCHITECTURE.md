# NAVARIS System Architecture

Mission: Need / Problem -> Evidence -> Qualification -> Diagnosis -> Opportunity -> Partner -> Action -> Contract -> Cash -> Learning.

## Layers
1. Control Center: single daily operating interface.
2. Orchestrator: selects the minimum required workflow and agents.
3. Agents: specialist workers.
4. Skills: reusable procedures and domain methods.
5. Engines: financial, feasibility, strategy, operations, quality, commercial and risk logic.
6. Data/Evidence: companies, contacts, opportunities, documents, sources, assumptions, KPIs and decisions.
7. Automations: scheduled reviews, intelligence and reminders.
8. QA: calculation, evidence, completeness and consistency testing.
9. Human Gate: approval before external communication, submission, contracting, purchasing, investing or commitments.

## Canonical lineage
FACT -> SOURCE -> CALCULATION -> ASSUMPTION -> INTERPRETATION -> RISK -> ACTION

## Operating states
NEW -> CAPTURED -> VALIDATING -> QUALIFIED -> ANALYZING -> READY_FOR_HUMAN_REVIEW -> APPROVED_FOR_ACTION -> IN_EXECUTION -> COMMERCIALIZED -> CASH_COLLECTED -> CLOSED/LEARNED

## Core objects
Company, Contact, Need, Opportunity, Partner, Supplier/OEM, Competitor/Peer, Tender/RFQ, Project, Document, Evidence, Financial Period, KPI, Task, Decision, Action, Cash Event.

## Design rules
- Cash-first: every commercial workflow has a route to measurable cash.
- Evidence-first: unsupported facts are never presented as facts.
- Single source of truth: avoid duplicate records.
- Explainable: scores expose inputs and reasoning.
- Modular: components can be replaced without redesigning the whole OS.
- Private-first: core logic can later support a local/private edition.
- Human-controlled: agents prepare and analyze; the user controls consequential action.

## AI Agent Coordinator
NOVA is the single coordinator. Specialist roles are routed on demand; they are not described as separately deployed autonomous services unless implementation and tests prove that status. The canonical role matrix, tool mapping, current evidence screen and run sequence are maintained in `docs/AI_AGENT_COORDINATOR_PLAN_2026-10-10.md`.

Routing order:
1. Review current pipeline and sent/reply history.
2. Demand/tender research from primary sources.
3. Evidence and eligibility QA.
4. Buyer/decision route.
5. Supplier qualification only after demand passes G0-G2.
6. Commercial match and written NAVARIS role.
7. Cash/risk evaluation with sourced inputs.
8. Reporting and archive.
9. Human Gate before consequential external actions.

One active master mission only. Existing daily task `NAVARIS Daily Tender-to-Cash` is the orchestration schedule. Do not create duplicate master automations. Zoho remains unavailable for live records until its OAuth scope mismatch is resolved.
