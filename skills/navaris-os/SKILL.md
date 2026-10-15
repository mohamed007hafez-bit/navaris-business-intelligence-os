# NAVARIS OS — Fixed Operating Skill

**Status:** Core methodology fixed; changes to formulas or thresholds require an explicit versioned change request.

## 1. Operating sequence

1. **Scout** — collect tenders/opportunities from user-supplied or locally saved sources. A sample record is not a live tender.
2. **Price** — calculate cost, profit, revenue split, ratios, and margin.
3. **Evaluate** — grade the margin and apply NAVARIS's simplified BCG-style banding.
4. **Qualify evidence** — identify buyer, supplier/OEM, RFQ, scope/specification, territory, price validity, delivery, payment terms, source URL/date, and verification status.
5. **Agreement gate** — prepare a non-binding NCNDA discussion draft only when a qualified opportunity reaches the configured grade and a counterparty is supplied. Legal review and authorized signatures are mandatory.
6. **Cash monitor** — separate invoice forecasts from cash actually collected. Forecasts are never recorded as collected cash.
7. **Cloud gate** — local-only by default. Cloud eligibility requires grade ممتاز, an explicit human approval flag, and local opt-in NAVARIS_ALLOW_CLOUD=1. The gate itself does not send data or make a network request.
8. **Decision / action** — GO, VERIFY, HOLD, or NO-GO based on evidence, economics, risk, terms, and authorization.

## 2. Fixed formulas

- Cost = Distance × Fuel/Route Rate + Toll + Surcharge
- Profit = Selling Price − Cost
- NAVARIS Share = Selling Price × 30%
- Operating Company Share = Selling Price × 70%
- Operating Company Net = Operating Company Share − Cost
- Gross Margin % = Profit ÷ Selling Price × 100 (0 when selling price is zero)
- Operating Ratio % = Cost ÷ Selling Price × 100 (0 when selling price is zero)
- Company Net % = Company Net ÷ Company Share × 100 (0 when company share is zero)

The 30/70 arrangement is the supplied skill's example model, not a universal entitlement. Use only when expressly agreed in writing by the parties.

## 3. Margin grades (fixed)

| Gross margin | NAVARIS grade |
|---:|---|
| Below 20% | غير مقبول |
| 20% to below 30% | مقبول |
| 30% to below 40% | جيد |
| 40% to below 50% | جيد جدا |
| 50% or higher | ممتاز |

## 4. NAVARIS simplified BCG-style bands (fixed)

| Gross margin | Band | Default posture |
|---:|---|---|
| Above 50% | STAR | Review for GO only after evidence and risk gates |
| 40% to 50% | CASH COW | Continue qualification |
| 20% to below 40% | QUESTION | Recheck assumptions and terms |
| Below 20% | DOG | Normally NO-GO / renegotiate |

This is a margin-based NAVARIS prioritization adaptation, not the original BCG market-growth/relative-share matrix.

## 5. Evidence standard

Every material claim must follow:

**FACT → SOURCE → CALCULATION → ASSUMPTION → INTERPRETATION → RISK → ACTION**

Allowed status values include VERIFIED, UNVERIFIED, ILLUSTRATIVE, UNKNOWN, and NOT CALCULABLE. A record is never verified just because a text field contains the word “verified”; a human must explicitly confirm its evidence status.

## 6. Local Hybrid security

- Local-first; no cloud or external data collection by default.
- Do not hard-code passwords, tokens, API keys, or private credentials.
- Keep .env, local databases, private client data, and generated output out of Git.
- The cloud bridge is a policy gate only. It does not implement a provider connection or upload data.
- Do not send client information to a cloud provider without explicit approval of the exact data and purpose.
- Never submit tenders, contact counterparties, send agreements, make commitments, or record cash receipts automatically.
- Generated NCNDA material is a discussion draft, not legal advice or an executable contract.

## 7. Core-file control

navaris_core.py is the fixed calculation engine. Do not edit its formulas or thresholds during ordinary feature work. Add tests and request a versioned change if a formula needs to change. Agents should call the core instead of duplicating calculations.

## 8. Execution commands

- Windows: double-click run_navaris_local.bat
- macOS/Linux: run bash run_navaris_local.sh
- Manual: python main.py --demo
- User-provided records: python main.py --input-json data/navaris_demo_input.json
- Tests: python -m unittest discover -s tests -v

Demo figures in the supplied source (including the example routes and monthly projection) are illustrative until replaced by source-backed, current evidence.
