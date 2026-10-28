# NAVARIS Enterprise Intelligence OS — Attraction & Authority Master Blueprint
Version 1.0 | 2026-10-28 | Status: Operating policy / implementation blueprint

## 1. Strategic mandate
Position NAVARIS as an evidence-led coordination and execution partner for energy procurement, oilfield technical services, freight/customs coordination, business diagnostics, QMS improvement, and AI-enabled operations. The objective is qualified inbound demand—not mass outreach or unsupported prestige claims.

Markets: Egypt first; Oman and GCC only when local partner capability, legal/compliance requirements, and delivery economics are verified.

## 2. Positioning architecture
### Master promise
"Clearer energy procurement and cross-border operations—through evidence-led qualification, disciplined coordination, and measurable commercial decisions."

### Attraction system
1. **Lamp (authority assets):** focused landing pages, practical checklists, source-backed explainers, landed-cost calculators, vendor-readiness checklists, and anonymized case studies.
2. **Moths (high-intent demand):** OEMs, regional operators, EPCs, subcontractors, procurement and logistics decision-makers who have a defined operational need.
3. **Nexus (conversion):** a qualification form capturing company, authorized contact, scope/specification, location, required date, budget/quote status, compliance documents, and consent.
4. **Proof gate:** no savings, mobilization, certification, portfolio value, or relationship claim published without a traceable evidence record.
5. **Qualified handoff:** only complete and verified opportunities move to commercial review; no automated promise, bid submission, or external message without an authorized approval step.

### Public copy — approved baseline
" NAVARIS helps energy and industrial teams structure procurement, equipment readiness, and logistics coordination across Egypt and selected regional markets. We qualify the requirement, identify evidence gaps, map the delivery path, and document the commercial decision before execution."

### Audience-specific value propositions
- **International OEMs:** regional requirement qualification, documentation readiness, buyer/partner fit checks, and local coordination—scope subject to verified capability.
- **Upstream operators / EPCs:** structured requirement intake, equipment/service readiness checklist, responsibility map, and evidence-backed timing assumptions.
- **Freight/customs partners:** better-defined shipment data, document checklist, landed-cost comparison, and exception escalation.
- **Business/QMS/automation clients:** documented baseline, explicit formulas, process controls, and reproducible results; no certification or audit outcome guarantee.

## 3. Evidence and claim registry
Every public claim must be stored as: claim_id, exact wording, claim type, source URL/file, source owner, date, scope, calculation, approval status, expiry/review date.
- **$20.7M portfolio:** unpublished until ownership/mandate, currency, portfolio composition, value date, and permission to disclose are evidenced. Distinguish "tracked opportunity value" from "contracted portfolio" and "collected revenue."
- **22% cost reduction:** a target/hypothesis until comparable baseline and new costs exist.
- **3-hour mobilization:** an SLA only when provider availability, geography, equipment, crew, permits, HSE/site access, clock definition, exclusions, and remedy are contractually agreed and testable.
- **25-year customs pipeline / Nafeza-ACI mastery:** require dated proof of relevant experience, named authorized partner, service boundary, and current procedural references.
- **ISO 9001:** state only the exact, current, verifiable credential or service scope. Never imply NAVARIS is certified or accredited unless a current certificate and issuing body are verified. Do not represent ISO 9001:2026 as a verified certification basis without official publication and status evidence.
- **Tier-1 client names:** list as target accounts only unless a documented client/contract relationship and disclosure permission exist.

## 4. Formula-first decision standard
For every analytical task, show the formula/model before applying it.
- Cost reduction % = (baseline comparable cost - new comparable cost) / baseline comparable cost × 100%.
- Current ratio = current assets / current liabilities.
- EBITDA margin % = EBITDA / revenue × 100%.
- Working capital = current assets - current liabilities.
- Asset-light ROIC: NOPAT / average invested capital. Define NOPAT and invested capital consistently; if invested capital is near zero or negative, disclose that ROIC may be misleading and use complementary measures.
- Opportunity qualification: use a published rubric with defined fields and weights; do not invent a universal formula. Missing critical fields mean "needs evidence", not a passing score.
Every result carries inputs, units, period, source, assumptions, calculation, limitations, and validation.

## 5. Clean data architecture — one source of truth
Canonical records:
1. Account: one stable account_id; legal name, country, domain, segment, verified contacts, consent/legal basis, status.
2. Need/Opportunity: one opportunity_id; buyer account, unique requirement/specification, delivery location/date, budget status, evidence, stage, owner.
3. Supplier/Capability: one supplier_id; legal identity, capacity, certifications, scope, location, validity dates, verification evidence.
4. Match: one match_id linking one requirement to one supplier/capability; spec fit, availability, compliance, commercial terms, evidence and reviewer.
5. Quote/Agreement: versioned documents, validity, scope, exclusions, approvals, counterparty signatories.
6. SLA: metric, clock start/stop, target, exclusions, responsible party, evidence source, breach route, acceptance.
7. Payment: invoice_id, amount, currency, due date, bank transaction reference, statement/evidence file hash, reviewer, verification timestamp, state.
8. Activity: one event per meaningful action; channel, idempotency key, outcome, consent/approval, next action.

De-duplication rules:
- Normalize legal name, email domain, phone, registration number, tender/notice ID, and supplier catalog/SKU before matching.
- Exact duplicates: same normalized stable identifier; merge references and preserve audit trail.
- Probable duplicates: similarity match; queue for human review, never auto-delete.
- Never deduplicate solely on display name, company name fragments, price, or similar text.
- Store canonical record plus aliases; do not erase historical activity, contracts, evidence, or audit events.

## 6. Workflow architecture
**Intake → Normalize → De-duplicate → Verify evidence → Qualify demand → Match supply → Commercial review → Written approval → Execute SLA → Invoice → Bank receipt verification → Close.**

One orchestrator owns stage transitions. Specialized agents may propose results but cannot self-approve:
- research agent: source capture only;
- qualification agent: completeness and fit;
- shipping agent: calculations from sourced inputs;
- oilfield agent: readiness checklist, not operational authorization;
- financial agent: metrics from supplied figures, not audit opinion;
- compliance/QMS reviewer: checklist and evidence review, not certification decision;
- commercial approver: pricing/contract authorization;
- finance verifier: bank-statement evidence review and cash status.

## 7. Bank-receipt-only cash control
States: LEAD → QUALIFIED → MATCH_VERIFIED → COMMERCIAL_APPROVED → AGREEMENT_SIGNED → INVOICED → PAYMENT_PENDING → BANK_RECEIPT_VERIFIED → CASH_COLLECTED.
- Quotes, POs, signed contracts, invoices, screenshots of transfer instructions, verbal confirmations, and forecasts are not collected cash.
- A transaction becomes CASH_COLLECTED only after a finance-authorized reviewer verifies a posted bank credit against the expected amount/currency, payer, date, bank reference, and invoice/agreement.
- Preserve the evidence file securely, hash it, record reviewer and timestamp, and reconcile reversals/refunds.
- Do not allow an agent or inbound form to self-assert verified payment.
- Report booked/contracted/invoiced/forecast/collected as separate metrics.

## 8. Verified demand-supply matching
A match is valid only when the buyer need and supplier capability are independently evidenced and align on:
- equipment/service specification and certification;
- quantity/condition/compatibility;
- location, required date, capacity and availability;
- permits, HSE, customs and document requirements;
- price basis, currency, Incoterms/responsibility split where applicable;
- written consent to introduce parties and conflict/commission terms.
Missing any critical criterion = NEEDS_EVIDENCE, not MATCH_VERIFIED.

## 9. SLA automation
Before an SLA is active, require a signed scope, named accountable provider, availability confirmation, start/stop definitions, calendar/time zone, target, exclusions, dependencies, evidence capture, escalation route, and acceptance criteria. System may monitor timers and flag risk; it cannot manufacture readiness or promise performance. A breached SLA creates an exception record and alert, not an auto-claim of damages.

## 10. Automation controls / zero-waste policy
- Idempotency keys for inbound events, emails, tender notices, invoices, and bank transactions.
- Outbound communications default to DRAFT_ONLY; send only with explicit approved recipient, content, legal basis/consent, and approver.
- No auto-bidding, contract acceptance, pricing commitment, certification statement, or supplier/customer introduction without authorized approval.
- No secrets in repository; use environment secrets and least-privilege permissions.
- Log state changes and reasons; never silently overwrite source evidence.
- Retry only transient errors with bounded exponential backoff; quarantine persistent failures.
- Scheduled jobs should have one canonical owner per purpose, concurrency group, run summary, failure alert, and deduplication state.
- SQLite placeholder is not a confidential production datastore; implement access controls, encrypted storage, backups and restore tests before sensitive use.

## 11. Funnel and KPIs
Primary metric: bank-confirmed cash collected.
Leading metrics: qualified inbound requests, evidence completeness %, verified demand-supply matches, proposal-to-agreement conversion, time-to-qualification, SLA attainment, gross contribution per deal, days sales outstanding, duplicate rate, unsupported-claim count.
Definitions:
- Evidence completeness % = required fields with valid evidence / total required fields × 100%.
- Match verification rate = matches passing all critical checks / matches reviewed × 100%.
- SLA attainment % = eligible SLA events met / eligible SLA events completed × 100%.
- Duplicate rate = confirmed duplicate records / records reviewed × 100%.
Define numerator, denominator, time window and exclusions before reporting.
No vanity metric substitutes for cash collection or verified delivery.

## 12. 30-day execution
Days 1–3: inventory assets/workflows, hash files, label canonical/overlap/obsolete, create claim registry, freeze destructive deletion.
Days 4–7: choose one canonical Pages deploy, one quality gate, one desktop build, one tender monitor and one PDF ingestion pipeline after checking triggers and required outputs.
Days 8–14: introduce canonical IDs, idempotency keys, evidence schemas, and duplicate review queue; run in report-only mode.
Days 15–21: add payment verification states and demand-supply/SLA gates with tests; keep approval required for external actions.
Days 22–30: measure inbound quality, match quality, SLA performance and bank-confirmed cash; retire duplicate workflows only after replacement is green and rollback path is documented.

## 13. Acceptance criteria
- One canonical public index path.
- Every workflow has a named owner and unique purpose; no competing deploy/build jobs trigger on the same event without a documented reason.
- No duplicate is hard-deleted without hash/provenance review and recoverable archive.
- Every public metric has an evidence-registry entry.
- Every cash-collection event has bank proof + finance reviewer.
- Every verified match has buyer and supplier evidence.
- Every active SLA has signed scope and measurable clock/exception rules.
- Tests cover missing evidence, invalid payment claims, duplicate events, supplier mismatch, SLA prerequisites, reversals, and audit trail.
- External messages remain approval-gated.
