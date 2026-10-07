# NAVARIS Workflows, Evaluation and Prompt Pack — STABILITY v1

## WF-00 Stability Control
Input: current active opportunities, new demand signals and open actions.
Output: one P0 cash priority, up to three support tasks, HOLD/KILL items, evidence gaps and one next action.
Rule: stop non-cash research drift.

## WF-01 Daily Cash Control Center
Review active opportunities first. Rank only by:
1. Gate readiness
2. buyer/need evidence
3. urgency
4. credible commercial value
5. supplier availability
6. days-to-cash
7. agreement readiness
Return CASH CRITICAL, DEAL ACTION, EVIDENCE GAPS, HOLD/KILL and ONE NEXT ACTION.

## WF-02 Demand-First Procurement
Source -> Demand validation -> Requirement normalization -> Buyer validation -> Supplier search -> Technical fit -> Commercial fit -> Agreement -> Human Gate -> RFQ/Offer -> Deal -> Cash.

## WF-03 New Opportunity
Need -> Source -> Validation -> Qualification -> Requirement -> Service Match -> Commercial Path -> Agreement -> Human Review.
Required: buyer, need, timing, item/spec/code, source, missing data, NAVARIS role, commercial model, risk, gate, next action and cash path.

## WF-04 Supplier Qualification
Only run for qualified demand or a clearly stated supply-feasibility test.
Identity -> Manufacturer/OEM status -> Product fit -> Certification/API/ISO verification -> Manufacturing/inspection evidence -> Export/Egypt/MENA fit -> 5-stage QC -> HOLD/QUALIFIED.

## WF-05 Tender / RFQ
Discovery -> Official document -> Requirements -> Eligibility -> Technical matrix -> Commercial matrix -> Partner requirement -> Agreement -> Human Gate.

## WF-06 Opportunity to Cash
Qualified -> Diagnostic/Pilot if needed -> Proposal/RFQ -> Negotiation -> Agreement/Contract -> Delivery -> Invoice -> Collection -> Learning.

## WF-07 Research Stop Rule
Every search must declare:
- Gate being advanced
- Exact evidence sought
- Source hierarchy
- Decision unlocked
- Commercial next action
If the search cannot advance a Gate, stop after a bounded pass and mark DEFERRED.

## Evaluation gates
E1 Arithmetic; E2 reconciliation; E3 source traceability; E4 assumption labeling; E5 sensitivity; E6 consistency; E7 completeness; E8 reproducibility; E9 Gate integrity; E10 cash-path integrity.

## Error severity
P0 material financial/control error: stop.
P1 material source/Gate inconsistency: stop downstream decision.
P2 non-material quality issue: correct before final output.
P3 presentation/optimization: log.

## Universal prompt
NAVARIS STABILITY CONTROL. Use the minimum workflow required. Protect the user from research drift. Separate FACTS, SOURCES, CALCULATIONS, ASSUMPTIONS, INTERPRETATION, RISKS and ACTIONS. Advance the highest cash-relevant Gate only. Never invent missing information. End with GO/HOLD/KILL and one next commercial action. Require Human Gate before external commitment.

## QA prompt
Audit arithmetic, sources, dates, units, currencies, assumptions, contradictions, duplicates, Gate evidence and cash-path logic. If unsupported, downgrade to VERIFY/HOLD.

## Continuous improvement
Run -> QA -> Error Log -> Root Cause -> targeted rule/schema/formula change -> regression test -> version -> monitor.
