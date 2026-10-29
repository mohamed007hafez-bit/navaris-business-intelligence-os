# NAVARIS Core Engine — Central System Log
**Version:** 1.0.0 | **Repository:** https://github.com/mohamed007hafez-bit/navaris-business-intelligence-os | **Branch:** main

## Operating doctrine
**TARGET → QUALIFY → STRUCTURE → EXECUTE → COLLECT → REPEAT**. Primary KPI: **CASH COLLECTED**. Cash defaults to zero until a bank receipt is independently verified and reconciled. Forecasts, invoices, receivables, pipeline values and cash must remain separate.

## Canonical formulas
- **Operating Expense Ratio:** OER = (OPEX / Net Revenue) × 100. If Net Revenue ≤ 0, return NOT CALCULABLE.
- **Operating Margin:** (EBIT / Net Revenue) × 100. Negative EBIT is valid; if Net Revenue ≤ 0, return NOT CALCULABLE.
- **Intermediary commission:** planning default 15% × agreed deal-value basis. Not an entitlement or industry-standard claim; written terms must define basis, payer, tax, timing and conditions.
- Unknown inputs remain UNKNOWN. Never fabricate rates, contracts, licences, buyer intent, supplier approval or receipts.

## Nine independent NAVARIS verticals
| ID | Vertical | Scope / guardrail |
|---|---|---|
| consulting | Consulting | Strategy, diagnosis, turnaround and operating-model improvement. |
| audit | Audit | Evidence-based operational, financial and control reviews; no statutory authority implied. |
| training | Training | Corporate training, course design and capability development. |
| fund | Fund | Fund research and investor intelligence; no regulated fund-management claim. |
| shipping_agent | Shipping Agent | Agency coordination only with proper authority and evidenced appointment. |
| commercial_rep | Commercial Representation | OEM/supplier market entry and buyer development under written mandate. |
| nvocc | NVOCC | Applicable registration, authority and operating capability must be verified first. |
| iso | ISO / QMS | QMS implementation/audit support; certification only by an authorized certification body. |
| tourism | Tourism | Tourism and hospitality services subject to applicable licensing. |

## Five coordinating autonomous agents
1. **Research & Market Intelligence** — source-backed demand, buyers, tenders, suppliers and market signals.
2. **Business Diagnosis & Strategy** — business model, operating constraints, turnaround and value creation.
3. **Finance & Cash Integrity** — deterministic financial KPIs and separation of forecast, invoice, receivable and verified cash.
4. **Commercial & Deal Qualification** — buyer need, decision route, supplier fit, quote evidence and agreement path.
5. **Delivery, Risk & Quality** — scope, compliance gates, delivery readiness, milestones, evidence and corrective action.

These five agents form the coordination layer. Existing specialized agents/scripts are retained as implementation modules; this does not claim the repository contains only five agents.

## Evidence and approval protocol
Every material conclusion follows **FACT → SOURCE → FORMULA → CALCULATION → ASSUMPTION → INTERPRETATION → ACTION**. Store source URL, publication date, checked date, owner, scope and evidence reference. Distinguish FACT / INFERENCE / ASSUMPTION / VERIFY / UNKNOWN. Scores are triage, not win probabilities. External communications, tender submissions, binding quotes, orders, signatures and financial commitments require specific human approval. Regulated status, licences, exclusive mandates, assets under management and certification authority require current evidence.

## Canonical architecture
- `navaris_core_engine.py`: deterministic formulas and machine-readable registry.
- `tests/test_navaris_core_engine.py`: formula, cash-gate and registry tests.
- `index.html`: public website; canonical title enforced by Quality Gate.
- `.github/workflows/navaris-quality.yml`: quality checks and core-engine tests.
- Existing `agents/`, `navaris_agents/`, `core/`, `engines/`, `formulas/`, `automation/` and other modules remain preserved until audited and migration verified.

## Audit limitations
This log centralizes definitions; it does not prove that all historical chats are present, all scripts are merged, the full commit history has been exhaustively reviewed, all workflows pass, or Pages has deployed the latest commit. Confirm those outcomes from GitHub Actions and Pages after each commit.
