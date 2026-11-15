# NAVARIS Business Intelligence OS

**Product owner:** Dr. Mohamed Hafez Khalifa, DBA  
**Professional brand:** Dr. Mohamed Hafez for Consulting & Operations Management  
**Repository:** navaris-business-intelligence-os

## Product purpose

NAVARIS is a local-first business intelligence and operations toolkit supporting evidence-led opportunity discovery, commercial qualification, operational and financial analysis, proposal drafting, workflow control, and cash-collection tracking.

Its initial operating focus is Egypt and relevant MENA markets across upstream oil and gas, well services, maritime logistics, freight forwarding, and selected consulting and operations-management engagements.

The business model is asset-light. The software supports research, analysis, coordination, and controlled execution; it does not itself create client relationships, supplier eligibility, contracts, revenue, or collected cash.

## Production status — read before use

**Repository status: active development; production readiness is not yet certified.**

A GitHub repository, a successful CI run, a generated workbook, or a published website is not by itself evidence that the complete business operating system is production-ready.

The system must pass the automated quality gate and the operational controls documented in docs/PRODUCTION_READINESS_GATES.md. In particular:

- CASH COLLECTED = 0 unless a bank receipt has been independently verified, reconciled to the correct transaction, and approved by an authorized human reviewer.
- A receipt reference or a user-entered boolean is not bank evidence.
- Forecasts, quotations, contracts, invoices, receivables, and cash received must remain separate values.
- Demand-supply matches remain recommendations for human review; they do not authorize orders, commitments, or payments.
- No external email, quotation, RFQ, tender submission, contract, purchase, investment, or other binding action may be made without explicit written owner approval.
- Demo inputs are illustrative and must never be represented as actual customers, live demand, verified rates, or collected cash.

## Repository map

| Component | Actual location | Purpose |
|---|---|---|
| Core local CLI | main.py | Builds the local analytical workbook from demo or supplied JSON input |
| Core engine | navaris_core_engine.py, engines/ | Deterministic calculations and business rules |
| Agent modules | agents/, navaris_agents/ | Research, financial, operational, routing, and control modules |
| Specialist toolkits | toolkit/, skills/ | Calculators, guides, templates, and skill instructions |
| Local web application | app/ | Next.js application and Supabase schema |
| Desktop shell | desktop/, cross-platform/, root package.json | Electron/Tauri-related application shells and build configuration |
| Operational data and schemas | data/ | Demo inputs, ledgers, and data schemas; do not put confidential client data in this public repository |
| Automated tests | tests/ | Regression, control, and calculation tests |
| Workflow definitions | .github/workflows/ | CI, build, report, and scheduled workflow definitions |
| Master workflow | docs/workflows/NAVARIS_MASTER_WORKFLOW.md | Evidence-to-cash process, decision gates, and human approval rules |
| Legal drafts | Legal Contracts & Protection Pack.md, templates/contracts/ | Draft templates only; legal review is required |

The demand-supply methodology is documented in Demand-Supply Scaling Engine.md; the legal framework is Legal Contracts & Protection Pack.md. Workflow names and paths in older documents may be historical; the repository tree and active workflow files are authoritative.

## Local quick start — Python core

Use Python 3.12 or a compatible supported version.

    python -m venv .venv
    # Windows:
    .venv\Scripts\activate
    # macOS/Linux:
    source .venv/bin/activate
    python -m pip install --upgrade pip
    python -m pip install -r requirements.txt -r requirements-dev.txt
    python main.py --demo --output output/NAVARIS_DEMO.xlsx
    python -m pytest -q

The demo creates illustrative output only. To use supplied data, provide a JSON file matching the expected input structure:

    python main.py --input-json path/to/input.json --output output/NAVARIS_ANALYSIS.xlsx

No live market data is fetched by this CLI unless a separately configured and approved integration is implemented.

## Supervised operating loop

1. Discover a company, tender, buyer request, supplier, or operational bottleneck.
2. Capture source URL, source date, retrieval date, and evidence reference.
3. Verify identity, authority, specification, location, eligibility, and commercial terms.
4. Run deterministic calculations with units, currency, period, formula version, and assumptions.
5. Qualify the opportunity and assign GO / HOLD / KILL with a reason and next action.
6. Prepare a non-binding offer or contract draft for human review.
7. Obtain written approval before any external action or commitment.
8. Track contract, invoice, receivable, and reconciled cash as separate records.
9. Review conversion, margin, cycle time, risk, and cash collection.

See docs/workflows/NAVARIS_MASTER_WORKFLOW.md.

## CI and release evidence

The supervised quality workflow validates Python modules, runs the automated test suite, builds a demo workbook, and uploads the generated workbook as a CI artifact. A green run proves only that the checks in that run passed for that commit. It does not prove live integrations, production deployment, customer usage, bank connectivity, or commercial performance.

No workflow in this repository is authorized to send client communications, submit tenders, issue binding quotations, sign agreements, make purchases, or record unverified cash.

## Security and data handling

This repository is public. Never commit passwords, API keys, tokens, bank statements, unredacted receipts, customer personal data, confidential quotations, or private deal records. Use synthetic or redacted test data. Review SECURITY.md before enabling integrations.

## Core KPI

**CASH COLLECTED** — actual funds received, independently evidenced, reconciled, and approved. Until that evidence exists, the recorded value remains zero.
