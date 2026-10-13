# NAVARIS Task Operating System

## Objective
Convert NAVARIS from a chat-first interaction model into a task-first operating model where every business request becomes a controlled task with planning, execution, evidence, validation, result, and next action.

## Core Flow

**INTAKE → QUALIFY → PLAN → EXECUTE → VALIDATE → HUMAN GATE (when required) → DELIVER RESULT → LOG → NEXT ACTION**

The chat interface is optional. It is a control surface, not the operating system.

## Task Lifecycle

- `DRAFT` — task captured but not ready.
- `READY` — inputs and acceptance criteria are sufficient.
- `RUNNING` — agent/workflow is executing.
- `WAITING` — blocked by an external dependency or scheduled condition.
- `HUMAN_GATE` — a consequential decision or external action requires owner approval.
- `COMPLETED` — acceptance criteria passed and result delivered.
- `FAILED` — execution failed; retry or escalation required.
- `CLOSED` — intentionally stopped, rejected, duplicated, or no longer commercially relevant.

## Task Object

Every task must contain:

1. Objective
2. Business value / CASH impact
3. Priority
4. Source / trigger
5. Inputs and evidence
6. Constraints
7. Assigned agent / workflow
8. Planned actions
9. Execution state
10. Validation checks
11. Human-gate requirement and decision
12. Result / artifacts
13. Risks / exceptions
14. Next action
15. Owner
16. Created / updated timestamps
17. Audit trail

## Agent Runtime Mapping

The reference runtime architecture maps into NAVARIS as follows:

**Task Input → Task Gate → NAVARIS Agent Core → Skills → Execution Loop → Hooks / State Validation → MCP / Connectors → Result**

- **Task Gate:** validates objective, permissions, inputs, priority and external-action policy.
- **Agent Core:** selects the workflow and coordinates specialist agents.
- **Skills:** deterministic business playbooks stored as versioned instructions.
- **Execution Loop:** performs repeatable steps and retries recoverable failures.
- **Hooks:** validate state, enforce duplicate guards, checkpoints and stop conditions.
- **MCP / Connectors:** provide controlled access to Outlook, GitHub, files and future business systems.
- **Human Gate:** blocks consequential external actions such as sending sensitive replies, submitting bids, signing, purchasing, investing or committing funds.
- **Result:** produces evidence-backed output, status, KPI impact and next action.

## NAVARIS Priority Queue

1. Cash due / collectible now
2. Active buyer ↔ NAVARIS ↔ seller / partner opportunities
3. Live RFQ / tender deadlines
4. Qualified buyer / supplier / representation opportunities
5. Training and consulting opportunities
6. Intelligence / research tasks
7. Internal system improvement

## Example: Outbound Follow-up

**Trigger:** outbound email thread has no substantive reply for >=24 hours.

**Workflow:**

1. Read original message and all subsequent replies.
2. Classify thread: active, substantive reply, rejection, unsubscribe, bounce, OOO, or no response.
3. If substantive reply / rejection / unsubscribe / bounce: stop.
4. If OOO has a return date: wait until return date plus the configured follow-up window.
5. If no substantive reply and >=24 hours: generate opportunity-specific follow-up.
6. Duplicate guard: never send more than one follow-up in the same 24-hour interval.
7. Send only if the configured automation policy allows it; otherwise create `HUMAN_GATE`.
8. Record sent time, message type, thread state, next follow-up date and opportunity value.
9. Continue daily until substantive response or explicit closure.

## Result Standard

A completed task must answer:

**WHAT HAPPENED → WHAT WAS VERIFIED → WHAT WAS PRODUCED → WHAT IS THE COMMERCIAL IMPACT → WHAT HAPPENS NEXT**

## Evidence Standard

Use:

**FACT → SOURCE → CALCULATION → ASSUMPTION → INTERPRETATION → RISK → ACTION**

## KPI

Primary KPI: **CASH COLLECTED**

Supporting task KPIs:

- tasks completed
- execution success rate
- human-gate queue size
- time to result
- qualified opportunities created
- follow-up response rate
- opportunities advanced
- deals won
- cash value influenced

## Design Rule

Do not build a feature merely because it is technically possible. Every task, agent, connector and screen must trace to a measurable business outcome and preserve an auditable execution trail.


## NAVARIS Three-Party Skill / Agent Routing (user mandate, 2026-10-13)

**Commercial position:** DEMAND / BUYER → NAVARIS → SUPPLIER / SERVICE PARTNER. NAVARIS remains the intermediary responsible for qualification, coordination, relationship structure and documented commercial value. The Agent Coordinator presents the full match to the user before any external action.

| Stage | Skill / playbook | Specialist Agent | Exit evidence |
|---|---|---|---|
| 1. Demand discovery | Demand Discovery | Demand Intelligence Agent | Current official need/RFQ/tender and source URL |
| 2. Buyer eligibility | Buyer & Eligibility | Buyer Qualification Agent | Buyer identity, decision route, deadline, eligibility and registration |
| 3. Scope extraction | Requirement Extraction | Technical Requirement Agent | Exact specifications, quantities, certifications, location, timing and terms |
| 4. Supply verification | Supplier Qualification | Supplier/OEM Agent | Specific supplier, exact fit, authorization, territory, certificates, availability, lead time and written terms |
| 5. Three-party structure | Three-Party Match | NAVARIS Match Agent | Buyer ↔ NAVARIS ↔ Supplier route, lawful role and agreement path |
| 6. Commercial feasibility | Commercial Economics | Cash/Risk Agent | Sourced fee/margin equation, payment and risk review; missing data = NOT CALCULABLE |
| 7. Draft outreach | Outreach Preparation | Communications Agent | Buyer/contracting-office and supplier/prime drafts; never sent automatically |
| 8. Evidence QA | Evidence & Compliance | Evidence QA Agent | Direct source links, freshness, contradiction and FACT/CLAIM/INFERENCE/UNKNOWN labels |
| 9. Final presentation | Coordinator | Agent Coordinator | Deduplicated decision package and SEND / DO NOT SEND gate |

Do not create a new database/workbook merely to represent agents. Use the existing master registry and existing automation.

### Coordinator's mandatory user-facing result
Two main sections only:
A. ANALYSIS → EQUATION → EVALUATION.
B. COMMERCIAL OPPORTUNITY → DECISION PACKAGE, including buyer, official demand, exact need, deadline, eligibility, supplier status, NAVARIS role, economics, risks, draft message and GO/HOLD/NO-GO.
Finish each external-action package with PREPARED FOR USER REVIEW — SEND / DO NOT SEND. The user is not asked to design the workflow. No external send, bid, binding quote, purchase, signature or commitment without explicit approval for that specific action.
