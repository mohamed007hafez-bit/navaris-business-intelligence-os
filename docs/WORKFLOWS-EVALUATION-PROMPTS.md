# NAVARIS Workflows, Evaluation and Prompt Pack

## WF-01 Daily Control Center
Review open opportunities, deadlines, expected cash, days-to-cash, missing follow-ups, new intelligence and QA flags. Return Cash-critical actions, Deal actions, Intelligence actions, Operational actions and Deferred items. Do not take external action.

## WF-02 New Opportunity
Need -> Intake -> Validation -> Qualification -> Diagnosis -> Service Match -> Commercial Path -> Human Review.
Required output: problem, buyer, timing, value, evidence, missing data, proposed NAVARIS role, risks, next action and cash path.

## WF-03 Company Diagnostic
Documents -> Extraction -> Validation -> Financial -> Operations -> Strategy -> Risk -> QA -> Executive Report.

## WF-04 Competitor / Peer Intelligence
NAVARIS target state -> market scope -> entity discovery -> source collection -> normalization -> factual comparison -> white space -> NAVARIS relevance -> QA.

## WF-05 Demand <-> NAVARIS <-> Supply
Demand capture -> qualification -> requirement normalization -> supply search -> technical fit -> commercial fit -> partner qualification -> Human Gate.

## WF-06 Tender / RFQ
Discovery -> document intake -> requirements -> eligibility -> technical matrix -> commercial matrix -> gaps -> partner requirement -> Human Gate.

## WF-07 Opportunity to Cash
Lead -> Qualified -> Diagnostic/Pilot -> Proposal -> Negotiation -> Contract -> Delivery -> Invoice -> Collection -> Learning.

## Evaluation gates
E1 Arithmetic; E2 accounting reconciliation; E3 source traceability; E4 assumption labeling; E5 sensitivity; E6 consistency; E7 completeness; E8 reproducibility.

## Error severity
P0 material financial/control error: stop. P1 material data/source inconsistency: stop downstream decision. P2 non-material quality issue: correct before final report. P3 presentation/optimization issue: log.

## Universal prompt
NAVARIS CONTROL CENTER. Analyze the request using the minimum required workflow. Separate FACTS, SOURCES, CALCULATIONS, ASSUMPTIONS, INTERPRETATION, RISKS and ACTIONS. Validate before concluding. Identify the route to CASH and the next action. Never invent missing information. Require Human Gate before any external communication, submission, contract, purchase, investment or commitment.

## Competitor prompt
NAVARIS COMPETITOR / PEER INTELLIGENCE. First lock the NAVARIS-only target state. Then map documented entities by offering, customer, geography, delivery model, commercial model, proof, partnerships, digital capability, gaps and NAVARIS relevance. Use dated evidence. Do not make unsupported superiority claims.

## QA prompt
NAVARIS QA. Independently audit the previous result for arithmetic errors, unsupported claims, stale sources, inconsistent units/currencies/periods, missing assumptions, contradictions, duplicates and incomplete actions. Classify findings P0-P3 and state required corrections.

## Continuous improvement
Run -> QA -> Error Log -> Root Cause -> Targeted rule/prompt/formula/schema change -> Regression Test -> Version -> Monitor.

## Global prohibition
Never fabricate clients, certifications, government relationships, exclusivity, financial results, partnerships, market facts or performance claims.