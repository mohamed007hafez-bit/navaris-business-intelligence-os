# NAVARIS Master Strategy & Execution Blueprint
**Version:** 1.0 | **Status:** Operating design; execution controls require tests and evidence | **Owner:** Founder / NAVARIS Business Operations & Development
**Geography:** Egypt, Oman and GCC, subject to local licensing, customs, tax, sanctions, procurement and partner-authorization checks.
**Operating doctrine:** TARGET → CASH 1ST → FLOW | DISCOVER → ANALYZE → QUALIFY → STRUCTURE → EXECUTE → COLLECT → REPEAT.

## 1. Executive decision
NAVARIS is an asset-light, evidence-led business operations and coordination platform. It does not represent itself as a buyer, funder, customs broker, carrier, certification body, or licensed operator unless the relevant legal capacity is documented. Revenue comes from approved scopes and disclosed brokerage/coordination arrangements, not from inflated transaction value.

The Lamp & Moths strategy means **publish useful evidence, tools, clear qualification criteria and a strong point of view** so relevant buyers and suppliers self-identify. It does not mean that tier-1 companies can be forced to approach NAVARIS or that inbound demand is guaranteed.

## 2. Formula-first decision rules
### 2.1 Cash conversion
Formula: `Cash Conversion Rate = Opportunities with verified bank receipt / Qualified opportunities × 100%`.
Use a defined cohort and period. Count only a bank receipt whose amount, currency, date, opportunity, redacted evidence reference, verifier and verification timestamp are recorded. PO, signed agreement, invoice, forecast, screenshot of a promise or expected commission is not collected cash.

### 2.2 Cost reduction
Formula: `Cost Reduction % = (Comparable baseline cost − comparable new cost) / comparable baseline cost × 100%`.
Compare the same scope, volume, period, currency, Incoterm, service level and cost categories. The 22% figure is a hypothesis until comparable quotations/invoices support it.

### 2.3 ROIC
Formula: `ROIC = NOPAT / Average invested capital × 100%`.
For an asset-light intermediary, record NAVARIS operating profit, taxes, working capital and actual invested capital. Portfolio value, gross merchandise value and partner turnover are not NAVARIS revenue or proof of ROIC.

### 2.4 SLA compliance
Formula: `SLA compliance % = eligible cases completed within the agreed SLA / all eligible cases due × 100%`.
A 3-hour mobilization target may be offered only for a defined service, start/stop clock, operating window, geographic boundary, exclusions, partner availability, evidence trail and written acceptance. Until validated, mark it **PROPOSED / UNVERIFIED**, never guaranteed.

### 2.5 Match integrity
A demand-supply match is actionable only when buyer identity and authority, live demand/RFQ, exact specification, quantity, destination, need-by date, supplier identity, eligibility, capacity, availability, quote validity, terms, documents and source evidence are verified. Any critical unknown = HOLD / REQUEST EVIDENCE, not a match.

## 3. Attraction architecture — one front door, three lanes
1. **Energy equipment & technical coordination:** Slickline/Wireline, PCE, well-intervention equipment, spare parts and technical talent. NAVARIS qualifies the requirement and coordinates verified counterparties; it does not imply inventory or operator approval without proof.
2. **Maritime, freight and customs readiness:** shipment-cost transparency, document checklists, Incoterms and Nafeza/ACI workflow readiness. Customs declarations and regulated activities are performed only by authorized parties. Do not claim 25 years of pipeline capability or “mastery” until supported by dated records and authorized-partner evidence.
3. **Business improvement, QMS and automation:** operational diagnostics, process mapping, internal audit support, KPI design, automation and training. Distinguish consultancy/gap assessment from independent certification. Use the applicable, verified edition of standards; do not advertise ISO 9001:2026 certification or authority without evidence.

## 4. Attraction funnel
**Public evidence → useful diagnostic/tool → structured intake → qualification → written scope → verified counterparties → approved commercial terms → execution evidence → invoice/payment request → bank receipt → benefits review.**

The website should attract with: a clear operational problem; a practical checklist/calculator; documented experience; transparent scope; proof register; response expectations; and a structured intake. Avoid manufactured scarcity, pressure tactics, unverifiable ROI, fake logos, or claims that customers will be “forced” to approach.

### Inbound content pillars
- **Cost & delay:** landed-cost calculator, demurrage exposure worksheet, document-readiness checklist.
- **Equipment readiness:** RFQ completeness checklist, part-number/specification template, supplier qualification gates.
- **Governance & quality:** process audit readiness, NCR/root-cause workflow, evidence and corrective-action tracking.
- **Executive operations:** working-capital, throughput, lead-time and SLA dashboards with formula, source and caveat.
- **Case evidence:** publish only anonymized/authorized cases with baseline, intervention, outcome, period and proof.

## 5. Claims governance — mandatory before publication
All material claims must have a record in `docs/NAVARIS_CLAIM_EVIDENCE_REGISTER.md`. Required fields: claim, exact wording, claim owner, primary source, date/period, calculation, permission to disclose, limitations, reviewer and status.

Initial claim handling:
- “$20.7M locked portfolio”: **DO NOT PUBLISH** until portfolio composition, ownership, signed mandates, value definition, dates, currency, and evidence are verified. Do not call it revenue, NAVARIS-owned assets or cash without proof.
- “3-hour emergency mobilization”: **PROPOSED / UNVERIFIED** until route-level operating data, partner commitments, clock definition and exceptions are proven.
- “22% operational cost reduction”: **TARGET / UNVERIFIED** until matched baseline and outcome data support the calculation.
- “25-year customs clearing pipeline / Nafeza-ACI mastery”: **UNVERIFIED** until authorized-partner evidence, experience records and exact role are documented.
- “Ex-Halliburton”: do not publish unless employer/contracting relationship and wording are fact-checked. Current substantiated working biography may reference the founder's IOD Slickline/Wireline well-maintenance experience at Ras Shukeir in 2012–2013, subject to CV/evidence review.
- “Executive DBA”: use exact degree, institution and award date supported by the credential.
- “ISO 9001”: distinguish training, internal audit support, consultancy, auditor qualification and certification. Never imply NAVARIS can issue certification unless it is an authorized certification body.

## 6. One source of truth — canonical records
Use one logical record per entity, not one file per workflow:
- `data/opportunities.json` or future CRM table: opportunity_id, legal entity, contact/source, live need, status, owner, next action/date, evidence links.
- `docs/suppliers-qualified.json` remains the current supplier qualification register until migrated; a supplier is qualified only when all defined gates are true and evidence is dated.
- `data/cash-collected.json` is the canonical repository-side cash ledger schema. Do not store bank account numbers or raw receipts in Git.
- `docs/cash-collected.json` is legacy schema; do not add new records there. Migrate only after schema validation and record-level reconciliation.
- One canonical commercial pitch and one channel adapter (email / WhatsApp / proposal); channel variants inherit the same approved claim register and scope.
- One canonical root website: lowercase `index.html`. Case-variant `Index.html` is legacy and must not be deployed.
- One workflow per purpose after the workflow retirement register is reviewed. Do not delete unique jobs just because their names look similar.

## 7. Automation and approval controls
- Default local-only, deterministic execution. Cloud AI and external sending are off by default.
- Every agent action must be explicit, typed, logged and reproducible; no action on import, no silent background side effects.
- No outbound email, WhatsApp, bid submission, booking, contract signature or binding quote without explicit founder approval.
- A verified match is a gate, not a probabilistic guess. Missing evidence returns HOLD.
- Cash ledger accepts only a verified bank receipt with redacted reference, verifier and timestamp. A user-supplied boolean is insufficient.
- SLA automation uses an agreed clock and evidence timestamps. Missing timestamps, paused-time rules or acceptance evidence returns UNVERIFIED.
- Log decision, input-source references, formula/model, output, status, reviewer and timestamp. Never commit confidential customer/bank data or credentials.
- SQLite in the core Electron app remains an unencrypted placeholder; do not store confidential records until security controls are implemented and tested.

## 8. Operating cadence
**Daily:** review new inbound requests; classify source/evidence; resolve missing fields; move qualified opportunities to a written scope; reconcile actual receipts.
**Weekly:** publish one useful evidence-led asset; review opportunity aging and next-action completeness; inspect match rejects and SLA breaches; remove duplicate content only after references are checked.
**Monthly:** review collected cash, contribution margin, DSO/aging where available, conversion rates, SLA compliance, case-study evidence and claim expiries.

## 9. KPI hierarchy
1. **Cash collected (bank-receipt verified)** — primary result.
2. Contribution margin on collected/earned engagements, calculated on consistent accounting basis.
3. Qualified live demand with evidence.
4. Verified demand-supply matches.
5. Approved written offers and conversion by cohort.
6. Time from complete intake to qualified decision.
7. SLA compliance on eligible cases.
8. Inbound-to-qualified rate by content/source.
9. Duplicate record rate and percentage of records with owner + next action.
10. Claim evidence coverage: published material claims with current approved evidence / all material claims published.

Never blend pipeline value, booked revenue, invoices, expected commissions and cash receipts into one “revenue” metric.

## 10. 30-day implementation sequence
- **Days 1–3:** freeze new overlapping templates; nominate canonical files; record legacy aliases; protect raw evidence and credentials.
- **Days 4–7:** reconcile opportunities, suppliers and receipts; deduplicate by stable IDs and normalized legal entity/domain; retain provenance; quarantine ambiguous records.
- **Days 8–14:** implement receipt, match and SLA gates with unit tests; leave all external side effects disabled.
- **Days 15–21:** publish one useful inbound tool and two evidence-backed technical notes; use approved claim register only.
- **Days 22–30:** measure inbound quality, qualification cycle, approved offers and collected cash; retire content/workflows only after CI and dependency checks.

## 11. Acceptance criteria
- No published unverified portfolio, savings, SLA, certification or employer claim.
- One canonical cash ledger and explicit legacy migration status.
- Every open opportunity has a stable ID, evidence, owner, next action and date.
- No demand-supply match becomes actionable with critical missing evidence.
- No cash is recognized from boolean flags alone.
- No SLA is reported as met without valid start/stop evidence and agreed clock rules.
- External side effects remain disabled unless specifically approved.
- Deduplication changes are logged, reversible and covered by tests.
