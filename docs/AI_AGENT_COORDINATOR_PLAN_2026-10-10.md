# NAVARIS AI Agent Coordinator — Cash-First Operating Plan
**Report timestamp:** 2026-10-10 15:47 Africa/Cairo (UTC+03:00)  
**Prepared by:** NOVA / NAVARIS AI Agent Coordinator  
**Identity:** Dr. Mohamed Hafez | NAVARIS | Business Operations & Development  
**Mission:** TARGET → CASH 1ST → FLOW | KPI: CASH COLLECTED

## 1. Operating decision
Use one coordinator and specialist agent roles, not multiple competing master tasks. The coordinator selects the smallest set of agents needed for each verified opportunity, checks evidence and duplicates, then returns a ranked action list. These are orchestration roles and prompts; they are not represented as separately deployed autonomous services unless the relevant runtime/workflow is actually implemented and tested.

**Commercial lane:** VERIFIED DEMAND → BUYER/DECISION PATH → QUALIFIED SUPPLIER → NAVARIS ROLE → WRITTEN AGREEMENT → OFFER/RFQ → DEAL → INVOICE → CASH → REPEAT.

## 2. AI agent coordination matrix
| # | Agent / role | Task and scope | Primary evidence/output | Skills / MCP / connected tools | Local program / GitHub asset | Gate / KPI |
|---|---|---|---|---|---|---|
| 0 | NOVA — Agent Coordinator | Choose one active priority; delegate bounded subtasks; prevent duplicates; merge findings; sequence next action | Daily master decision, agent assignments, ranked actions | NAVARIS Cash Engine skill; Automations MCP; GitHub MCP; Outlook MCP | `docs/AI_AGENT_COORDINATOR_PLAN_2026-10-10.md` | No parallel master missions; maximum 3 new targets |
| 1 | Demand & Tender Intelligence Agent | Find only current, open, relevant tenders/RFQs and documented buying signals in Egypt/Gulf first | Tender ID, buyer, scope, deadline, official URL, eligibility, submission path, bid bond/fees, status | Web search; official buyer portals; public e-procurement; NAVARIS cash skill | `scripts/build_agreement_first_os.py`; `.github/workflows/navaris-cash-flow-engine.yml` | G0 source + G1 demand; expired/unclear = HOLD |
| 2 | Buyer & Decision-Maker Agent | Verify buyer identity, need, urgency, public contact path and decision process | Buyer profile, need evidence, decision route, last verified date | Web; Outlook search/read; Zoho CRM after OAuth repair | Zoho Leads/Accounts/Deals tools (currently blocked by OAuth scope mismatch) | No assumed budget or decision-maker |
| 3 | Supplier / OEM Qualification Agent | Match suppliers to a verified spec; check manufacturer/distributor status, technical fit, lead time and certificates | Supplier evidence register, gap list, qualification status | Web; GitHub records; Outlook history; Zoho after OAuth repair | Supplier/QC records in NAVARIS workbook | G3 supply + G4 fit; no capability claims without proof |
| 4 | Opportunity Match & Commercial Structuring Agent | Match Demand ↔ Supplier ↔ NAVARIS service; define agency/representation/referral role and fee basis | Match table, route-to-market, written-agreement need, commission terms only when sourced/agreed | NAVARIS Cash Engine skill; Formula Genius; Outlook draft tools | `data/NAVARIS_3Part_AgreementFirst_OS.xlsx` | G5 written agreement before external commercial commitment |
| 5 | Consulting & Training Agent | Find a specific published business/operations/training need and build a scoped paid diagnostic or training offer | Target, signal, service scope, buyer route, pricing inputs, next action | Web; business-analysis/report skills; Outlook draft | Opportunity map / training library | No generic lead without need evidence |
| 6 | News-to-Signal Agent | Review energy, ports, freight, Hormuz/Red Sea, project and procurement news; translate only evidenced signals into targets | NEWS → SIGNAL → NEED → TARGET chain with source/date | Web; NAVARIS cash skill | `NEWS_SIGNALS` table or equivalent | News alone is not an opportunity |
| 7 | Cash, Risk & Feasibility Agent | Assess cash proximity, days-to-cash only when inputs exist, costs, eligibility, working capital and execution risk | GO / VERIFY / HOLD / NO-GO with transparent calculations | Formula Genius; business-analysis skill; workbook formulas | Cash calculator / gate scorecard | Actual Cash remains 0 until received and evidenced |
| 8 | Evidence & QA Agent | Verify source authority/freshness, duplicates, dates, calculations, assumptions, confidence and contradictions | Evidence chain and QA flags | Data quality + validate-data skills; web; GitHub MCP | `scripts/validate_navaris_workbook.py`; `SOURCE_REGISTER`; `RESEARCH_LOG` | FACT → SOURCE → CALCULATION → ASSUMPTION → INTERPRETATION → RISK → ACTION |
| 9 | CRM & Follow-up Agent | Maintain one pipeline; inspect sent/replies before follow-up; record status and next date | Contact/opportunity status, sent/replied/no-response, follow-up due | Outlook Email MCP; Zoho CRM when reauthorized | CRM and workbook pipeline | Never duplicate outreach; no external message without Human Gate where required |
| 10 | Reporting & Archive Agent | Produce dated concise report plus data tables, preserve source links, send internal archive to Gmail via Outlook | Executive summary, opportunity matrix, agent/task/software matrix, blockers, source log | Outlook send_email; GitHub MCP; workbook/PDF tooling when available | Daily report/archive; commit references | Report only files actually created; verify send result |
| 11 | Repository / Workflow Engineer Agent | Maintain skill instructions, scripts, GitHub Actions and tests; no risky workflow changes without inspection | Versioned change, commit SHA, validation evidence | GitHub MCP; GitHub Actions; Python/openpyxl | `scripts/build_agreement_first_os.py`; `scripts/validate_navaris_workbook.py`; `.github/workflows/navaris-cash-flow-engine.yml` | Never claim workflow passed unless run/test result confirms |

## 3. MCP servers / plugins and their use
| Connector / tool | Role in the coordinator | Current status / constraint |
|---|---|---|
| Microsoft Outlook Email MCP | Search sent/replies, create drafts, send internal reports to Gmail, archive correspondence | Read access verified today. Report email can be sent via Outlook; Gmail inbox delivery cannot be independently confirmed from Outlook alone. |
| GitHub MCP | Read/update repository files, save skills/plan, version changes | Repository accessible: `mohamed007hafez-bit/navaris-business-intelligence-os`. |
| Zoho CRM MCP | Leads, Accounts, Deals, activity/pipeline records | Connected but CRM query failed with `OAUTH_SCOPE_MISMATCH`; reconnect/reauthorize before using live records or writes. |
| Automations MCP | Maintain one daily master task and its schedule | Existing master automation: `NAVARIS Daily Tender-to-Cash`; update this task only; do not create duplicate NAVARIS master tasks. |
| Formula Genius MCP | Spreadsheet formulas, scoring, cash calculations and QA | Use only with sourced inputs; no invented budget, probability or commission. |
| Web research | Official tender portals, buyer/vendor pages, public notices, current market signals | Prefer official primary sources and record retrieval date. |
| WhatsApp Business / Zoho integration | Potential customer messaging channel | Not yet connected; check current-number compatibility and cost before any migration or setup. |

## 4. Existing repository programs and assets
| Asset | Intended job | Required verification |
|---|---|---|
| `skills/navaris-cash-engine/SKILL.md` | Cash-first operating rules, evidence gates, supplier QC, Human Gate | Updated to require coordinator + specialist-agent routing |
| `docs/SYSTEM-ARCHITECTURE.md` | Layering, object model, evidence lineage and control | Coordinator section links to this plan |
| `docs/STRATEGY_CASH_FIRST.md` | Commercial strategy and prioritization | Keep consistent with one active mission |
| `scripts/build_agreement_first_os.py` | Build the Excel agreement-first workbook and opportunity map | Run only in a tested environment; inspect outputs |
| `scripts/validate_navaris_workbook.py` | Validate workbook sheets/controls | Must pass before calling workbook validated |
| `data/NAVARIS_3Part_AgreementFirst_OS.xlsx` | Demand / NAVARIS service / supplier / agreement / evidence / cash operating data | Update with stable IDs; deduplicate before writes |
| `.github/workflows/navaris-cash-flow-engine.yml` | Scheduled GitHub Action for workbook controls | Existing workflow writes to workbook and commits; do not assume successful run without Actions evidence |

## 5. Initial opportunity screen — 2026-10-10
This is a source-backed screen, not a claim of contract, supplier match, revenue or cash. Only three targets are carried forward.

| Priority | Opportunity / status | Verified facts | NAVARIS fit | Assessment / risks | Next action |
|---|---|---|---|---|---|
| P1 | Alexandria Container & Cargo Handling Co. tender 2026/10 — OPEN on official page as checked today | Supply of steel wire ropes, locks and hooks for Alexandria terminal; technical-envelope opening 2026-10-21; initial security = 2% of bid; booklet EGP 342 | Supplier qualification / sourcing / commercial coordination if allowed by tender rules | **High urgency; medium feasibility until full tender document, specs, buyer eligibility, procurement rules and supplier fit are verified.** Do not submit or promise representation without a qualified supplier and written terms. | Download/read official booklet; verify exact quantities/specs, submission route, bid security basis, payment/delivery and whether third-party coordination is allowed; then check supplier responses already in Outlook. |
| P2 | Egyptian public e-procurement: gas turbine supply — VERIFY | Official portal listing shows tender published 2026-10-03, deadline 2026-10-26; listing title “Supply of gas turbines for electricity generation” | Possible equipment sourcing only if a qualified OEM/channel and eligibility path exist | **Low near-term cash fit** due to likely high technical/financial threshold and missing scope, budget and vendor requirements in listing snapshot. | Open full tender, obtain specs and eligibility; HOLD supplier search until requirements and submission rules are known. |
| P3 | Egyptian Ministry of Military Production procurement listings — VERIFY / watchlist | Official portal lists notices dated 2026-10-07 for sheet-steel plates and fasteners, and other spare-parts items; deadlines/specs not verified in the available listing | Possible industrial sourcing only after exact spec and deadline are available | **Low confidence / not yet qualified.** A listing alone does not establish NAVARIS access, margin or payment timing. | Open each notice and attached documents; retain only still-open, spec-clear, reachable opportunities. |

### Current evidence and links
- Alexandria Container & Cargo Handling tender page: https://alexcont.com/ar/tenders/
- Egyptian Public e-Procurement System: https://www.eps-gags.gov.eg/eb/operation/moveAnoncemtSuplrList.do?uperMenuId=EB01030000
- Ministry of Military Production tenders: https://www.momp.gov.eg/Ar/Tenders.aspx
- Aramco supplier portal / registration: https://www.aramco.com/en/what-we-do/suppliers
- Aramco contracting opportunities: https://www.aramco.com/contracting
- Egypt Mineral Resources Authority tender portal: https://emra.gov.eg/w/tenders-1 (site fetch failed during this pass; treat as inaccessible, not as evidence of no tenders)

## 6. Daily run sequence
1. Coordinator reviews current pipeline, recent Outlook sent/replies and prior report before new research.
2. Demand Agent checks official sources and identifies up to three new targets.
3. Evidence Agent verifies status, deadline, eligibility and source freshness.
4. Supplier Agent is activated only after demand/specification passes G0–G2.
5. Match/Cash Agent scores commercial fit and cash proximity using sourced inputs.
6. QA Agent checks duplicates, calculations and unsupported claims.
7. Reporting Agent sends one dated internal report from Outlook to `mohamed007hafez@gmail.com`.
8. Coordinator records status, exact blocker, next action and actual cash evidence. If no qualified new opportunity exists, report `NO MATERIAL NEW OPPORTUNITY` rather than padding.

## 7. Priority score and decision rules
Use qualitative GO / VERIFY / HOLD / NO-GO unless all scoring inputs are available. Compare: source confidence, verified demand, buyer access, technical fit, eligibility, written NAVARIS role, cash proximity, execution burden, payment risk, and days-to-cash. Never fabricate contract value, budget, probability, commission or expected cash. Record scenarios only with explicit assumptions and calculations.

## 8. Human Gate and control rules
- Agents research, analyze, draft, validate and recommend; they do not independently commit NAVARIS.
- Human approval required before external messages when the current task/rules require it, tender submission, quotation, purchase, agreement, representation, contract, investment or binding promise.
- No claim of “sent”, “connected”, “qualified”, “validated” or “cash collected” without tool/source evidence.
- CASH COLLECTED = actual funds received only.
- Preserve one active NAVARIS master mission; no duplicate automation or workflow.
