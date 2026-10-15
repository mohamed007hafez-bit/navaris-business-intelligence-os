# NAVARIS Business Intelligence OS

**Mohamed Hafez | NAVARIS | Business Operations & Development**

NAVARIS is an execution-oriented Business Operating System & Commercial Gateway designed to turn verified business problems and market needs into qualified commercial action and cash.

## Primary Objective

Build a controlled, modular decision and execution system connecting:

`VERIFIED DEMAND` ➔ `EVIDENCE` ➔ `REQUIREMENT` ➔ `QUALIFIED SUPPLY` ➔ `NAVARIS ROLE` ➔ `AGREEMENT` ➔ `EXECUTION` ➔ `CASH` ➔ `REPEAT`

**Primary KPI:** CASH COLLECTED

## Stability Rule

NAVARIS is not optimized for research volume, dashboards, CRM complexity, or generic consulting activity. During stabilization, the core operating lane is strictly bounded to:

`Demand` ➔ `Requirement` ➔ `Qualified EU OEM/Tier-2 Supply` ➔ `NAVARIS Commercial Role` ➔ `Agreement` ➔ `Offer/RFQ` ➔ `Deal` ➔ `Cash`

### Priority Assets
- Wells, refineries, ships, offshore platforms, and energy/industrial facilities.

### Priority Product Families
- Fishing Tools, Wellhead, BOP, API 610 Pumps, LPG Hoses (6" & 8" × 12m).
- *Note:* Closely related maintenance items are included only when concrete demand evidence supports them.

## Anti-Distraction Protocol

- **Focus:** One active cash priority at a time; maximum of three supporting tasks.
- **Research Boundary:** No broad research without a defined Gate and specific commercial action.
- **Supply Boundary:** No supplier search expansion before qualifying demand, except for a bounded supply-feasibility test.
- **Financial Rigor:** No unsupported price, commission, probability, or cash estimate.
- **Data Integrity:** `Unknown` = **VERIFY/HOLD** | Never use invented or unverified data as a `FACT`.
- **Termination Rule:** Every execution run must end with a clear status of **GO / HOLD / KILL** + exactly one next action.
- **The Human Gate:** A mandatory human review is required before issuing any external messages, tenders/RFQs, quotations, contracts, purchases, investments, or commercial commitments.

## Evidence Chain

`FACT` ➔ `SOURCE` ➔ `CALCULATION` ➔ `ASSUMPTION` ➔ `INTERPRETATION` ➔ `RISK` ➔ `ACTION`

## Gate System

`G0 SOURCE` ➔ `G1 DEMAND` ➔ `G2 REQUIREMENT` ➔ `G3 SUPPLY` ➔ `G4 FIT` ➔ `G5 AGREEMENT` ➔ `G6 ACTION` ➔ `G7 CASH`

- *Rule 1:* No Gate ➔ No Work.
- *Rule 2:* No Evidence ➔ No Gate.
- *Rule 3:* No Cash Path ➔ No GO.

## System Architecture

- `docs/` — Strategy, governance, stability, business model, and intelligence.
- `engines/` — Deterministic financial, feasibility, strategy, quality, operations, commercial, and risk logic.
- `agents/` — Controlled research, validation, analysis, and reporting workflows.
- `data/` — Data schemas, evidence tracking, commercial opportunities, sectors, and compliance standards.
- `formulas/` — Core formulas for finance, accounting, valuation, ratios, and break-even analysis.
- `templates/` — Commercial diagnostics, feasibility studies, strategy development, readiness assessments, and execution reports.
- `tests/` — Automated validation tests for formulas and commercial scenarios.
- `app/` — Task control interface and operational outputs.

## Data Privacy & Security

Sensitive client or transaction data must **never** be placed in a public repository. Utilize the minimum necessary data to process transactions and strictly preserve the Human Gate at all stages.

## Current Build Rule

Every single module, script, or documentation file must serve a measurable commercial purpose and trace back directly to the evidence chain. Technical functionality and coding aesthetics are strictly secondary to verified cash proof.

## NAVARIS Local Hybrid OS (Fixed Skill)

The supplied NAVARIS OS skill is implemented as a local-first Python engine with an editable Excel workbook and native Excel charts.

### Local quick start

- Windows: run `run_navaris_local.bat`.
- macOS/Linux: run `bash run_navaris_local.sh`.
- Manual demo: `python main.py --demo`.
- Regression tests: `python -m unittest discover -s tests -v`.

Core modules:
- `navaris_core.py` — fixed formulas, grading bands, and Excel chart generation.
- `scout_agent.py` — scores user-provided opportunities; examples are not live tenders.
- `pricer_agent.py` — route economics and 30/70 model.
- `ncnda_agent.py` — non-binding draft only, legal review required.
- `cash_agent.py` — projection separated from actual collected cash.
- `chatgpt_bridge.py` — local-only cloud eligibility gate; no network request is implemented.
- `main.py` — orchestrates the local run and creates `output/NAVARIS_Agnatics_OS_FINAL.xlsx`.

See `skills/navaris-os/SKILL.md` and `docs/NAVARIS-LOCAL-HYBRID-OPERATING-MANUAL.md` for the fixed methodology, setup, controls, and known limitations.

**Security:** No GitHub token is required by the local engine. No cloud request, tender submission, external email, or commercial commitment is made automatically. All demo values are illustrative until verified against source evidence. Local processing does not automatically encrypt files; enable full-disk encryption and protect client data at the operating-system level.
