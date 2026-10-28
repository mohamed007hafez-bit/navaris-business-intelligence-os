# NAVARIS Master Strategy & Execution Blueprint
Version 1.0 | 2026-10-28 | Evidence-gated operating policy | Formula First

## 1. Positioning
NAVARIS is an asset-light business-operations and coordination platform that qualifies energy-sector requirements, aligns buyers with capable suppliers, structures documented execution, and measures realized outcomes. Egypt is the operating base; Oman/GCC opportunities are accepted only when local route, partners, compliance and delivery capacity are evidenced.
Core proposition: Make complex energy procurement and cross-border operations easier to qualify, coordinate and audit—without claiming assets, licences, approvals or capacity NAVARIS does not control.
Attraction sequence: Evidence → Authority → Inbound Interest → Qualification → Verified Match → Written Agreement → Execution → Bank Receipt → Repeat. Attraction is not passive waiting: publish useful evidence, measure qualified inbound demand, and stop repetitive unsolicited follow-ups.

## 2. Proof ledger — block unsupported claims
Every public claim needs: claim_id, exact wording, owner, source URI, evidence file/hash, date checked, scope, region, expiry/review date, status and approved wording. Statuses: VERIFIED, DOCUMENTED_NOT_INDEPENDENTLY_VERIFIED, TARGET, UNVERIFIED, EXPIRED. Only VERIFIED may be stated as fact. TARGET must be labelled a target/scenario. UNVERIFIED and EXPIRED claims are blocked from public copy.

| Claim | Default until evidence is checked | Rule |
|---|---|---|
| $20.7M portfolio | UNVERIFIED | Do not say locked/managed without contracts, scope and authority evidence. |
| 3-hour emergency mobilisation | TARGET / UNVERIFIED | No guarantee unless a defined provider, region, operating window and contracted SLA are proven. |
| 25-year customs pipeline | UNVERIFIED | Verify timeline, entities, authorisations and role; do not imply NAVARIS holds a broker licence unless true. |
| Nafeza / ACI mastery | UNVERIFIED | Limit wording to evidenced coordination support and authorised party procedures. |
| ISO 9001 auditing/QMS | UNVERIFIED | Distinguish consulting, internal QMS support, auditor qualification, certification-body authority and certified status. |
| DBA/offshore experience | DOCUMENTED_NOT_INDEPENDENTLY_VERIFIED until checked | State exact credential/employer/role/dates supported by records; do not imply Halliburton affiliation beyond evidence. |
| 22% savings | TARGET / UNVERIFIED | Scenario only until like-for-like baseline and actual cost evidence substantiate it. |

## 3. Canonical offers (one per problem)
1. Energy Equipment Readiness Brief: specification, destination, required date, document list, supplier evidence and gaps.
2. Asset-light Logistics Coordination: quote comparison, landed-cost model, document handoffs, partner capacity and milestones. Do not misrepresent NAVARIS as carrier, customs broker or importer of record.
3. Operations & QMS Improvement Sprint: process map, risk/control register, KPI baseline, corrective-action tracker and evidence pack; no certification guarantee.
4. Automation & Management Intelligence: local-first workflows, traceable calculations, validated data and reporting.
5. Executive Business Diagnostic: decision, evidence, formula/model, options, economics, risks and implementation plan.
Each offer has one canonical description, intake form, qualification checklist, proposal, SOW, KPI definition and owner. Regional variations are parameters, not duplicate workflows.

## 4. Attraction content engine
Publish one evidence-led asset weekly: (1) landed-cost calculator with inputs/exclusions/source fields; (2) mobilisation-readiness checklist, not a time promise; (3) Nafeza/ACI document-readiness explainer reviewed by an authorised practitioner; (4) anonymised case study with baseline, method, actual result, limitations and permission. Each asset states audience, problem, formula/model, data date, assumptions, limits and one intake link. Avoid duplicate pitches with cosmetic title changes.

## 5. Qualification and demand-supply gates
QUALIFIED requires: identifiable buyer and authorised contact path; written scope/geography/need-by date; authority and budget/procurement path evidenced or marked unknown; supplier capability evidence where relevant; document/compliance list; comparable pricing inputs or NOT CALCULABLE; owner, next action, due date and source links. Unknown is not zero and not approval.
A match is eligible only if demand and supply have stable IDs; specification/quantity match; destination/date feasible based on current written confirmation; currency, Incoterms, quote validity, tax/customs assumptions and payment terms recorded; applicable licences/certificates/HSE checked; counterparty and legal restrictions reviewed; and permission to share information confirmed. Output MATCHED_FOR_HUMAN_REVIEW, never automatic execution. Agents may not sign, order or promise for a party.

## 6. Bank-receipt-only cash policy
Cash collected, commission KPI and payment status remain zero/NOT_CONFIRMED until receipt evidence is matched to a transaction and reconciled by an authorised reviewer or approved bank feed. Store receipt_id, transaction reference, value date, amount/currency, payer, beneficiary, invoice/contract reference, evidence URI/hash, status, reviewer and timestamp. States: DRAFT → INVOICED → PAYMENT_PENDING → RECEIPT_EVIDENCE_UPLOADED → RECONCILIATION_PENDING → RECEIVED_VERIFIED or REJECTED. Only RECEIVED_VERIFIED counts as cash. A screenshot/self-report alone is insufficient unless independently reconciled. Never store bank passwords or full card details.

## 7. SLA state machine
Start an SLA clock only after the contract-defined trigger is evidenced. Record timestamps/timezone, scope, provider acknowledgement, dependencies, exclusions, pauses and completion proof. States: NOT_COMMITTED → CAPACITY_CHECK_PENDING → CAPACITY_CONFIRMED → SLA_ACCEPTED_IN_WRITING → IN_PROGRESS → COMPLETED_EVIDENCE_PENDING → COMPLETED_VERIFIED; exceptions go to BREACH_REVIEW. No compliance rate if the SLA was not accepted or trigger/stop event is missing.

## 8. Formula First — formula before application
Cost reduction % = (Comparable baseline cost − new cost) / comparable baseline cost × 100%.
Landed cost = freight + duties/customs + handling + insurance + other evidenced cost lines.
Current ratio = current assets / current liabilities, when liabilities > 0.
Working capital = current assets − current liabilities.
EBITDA margin % = EBITDA / revenue × 100%, when revenue > 0.
Inbound conversion % = qualified inbound opportunities / total inbound enquiries × 100%.
Cash realization % = verified cash received / cash contractually due × 100%.
SLA compliance % = eligible SLA events completed within contracted threshold / all eligible SLA events × 100%.
Define units, period, denominator, scope, source and exclusions before calculating. For missing inputs, zero denominators or non-comparable data, return NOT CALCULABLE and explain why.

## 9. Clean architecture
- Intake: one canonical schema, unique lead_id and idempotency_key.
- Evidence registry: source links/hashes, status, owner and timestamps.
- Qualification: deterministic validation and explicit missing-input reasons.
- Matching: explicit rules; MATCHED_FOR_HUMAN_REVIEW or REJECTED_WITH_REASONS.
- Proposal/SOW: draft only until a human approves external sending; signed scope before execution.
- SLA monitor: evidence-backed event/state machine.
- Cash ledger: receipt-only verified status; append-only audit trail.
- KPI dictionary: one definition/source/owner/cadence per KPI.
- AI agents: assist and validate; never invent rates, receipts, certifications, approvals or consent.
- Data: current core SQLite is unencrypted. Do not store confidential customer/contract/banking data until access controls, backups, retention and planned encryption are implemented and tested. This blueprint does not claim encryption exists.

## 10. Repository de-duplication audit (28 Oct 2026)
Scope inspected: recursive Git tree; 16 YAML workflows under .github/workflows; root README, AGENT.md, agents.json, core agent router/config/database modules and Formula First protocol. External email, WhatsApp, shared drives and all Library files were NOT fully audited; no claim of global purge.

High-confidence overlaps:
- Root Windows installer: build-desktop.yml, desktop-build.yml, windows-build.yml and navaris-core-only.yml overlap on root installer build. Canonical automatic build: navaris-core-only.yml. Keep legacy workflows manual-only until canonical tests pass and rollback is documented.
- Pages deployment: deploy-pages.yml uploads the whole repository root; navaris-pages.yml assembles a restricted _site. Prefer navaris-pages.yml; root-wide publication increases exposure and risks competing deployments.
- navaris-quality-gate.yml requires founder.jpg (conflicts with core-only scope) and treats a failed npm build as non-fatal; it is not a reliable gate.
- pdf-auto-train.yml and pdf-train.yml validate different schemas/paths and both may write generated outputs. Select one data contract before allowing both to be authoritative.
- main.yml and navaris-cash-flow-engine.yml test overlapping legacy modules/workbooks but are not proven identical; retain pending ownership and coverage review.
- navaris-quality.yml validates legacy manifests; its gate ownership needs consolidation with core-only tests.
- Index.html and index.html coexist. Lowercase index.html is the Pages entry; inspect references before deleting the capitalised file.
- AGENT.md contains an older master/slave design and a hard-coded MASTER_KEY. Treat it as stale reference; never reuse the hard-coded key.

Safe purge rule: first make duplicate workflows manual-only; delete only after references, workflow history, canonical replacement and rollback are documented. No external emails or communication records were purged by this audit.

## 11. One KPI definition each
Qualified inbound opportunities; Qualification Rate = qualified/enquiries; Verified Match Rate = matches passing gates/qualified demand requiring supply; Proposal Acceptance Rate = signed SOWs/proposals issued; SLA Compliance; Cash Collected (verified bank receipt, primary KPI); Cash Realization; Gross Contribution with explicitly stated cash/accrual basis. Every KPI has one formula, source, owner, cadence and audit trail.

## 12. First 14 days
Days 1–2: freeze unsupported claims; build proof ledger and assign owners. Days 3–4: select canonical workflows and make duplicate jobs manual-only; test canonical paths. Days 5–6: unify lead/demand/supplier/match/contract/SLA/receipt IDs. Days 7–8: implement deterministic gates and tests. Days 9–10: publish calculator and readiness checklist with formula and assumptions. Days 11–12: measure qualified inbound, not vanity traffic. Days 13–14: run one real opportunity end-to-end, record bottlenecks and automate only proven steps.

## 13. Release acceptance
No quantitative public claim without evidence status/source; one canonical workflow per purpose; external proposals human-approved unless delegated authority is documented; match/SLA transitions require evidence; cash remains zero until reconciliation; formula precedes calculation; tests cover idempotency, missing receipt, invalid match, SLA edge cases and audit-log integrity.