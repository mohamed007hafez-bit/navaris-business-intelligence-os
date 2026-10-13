---
name: navaris-master-workflow
description: Run the NAVARIS evidence-led, cash-first business workflow from discovery through analysis, qualification, approved execution, invoicing, collection, and KPI review. Use for workflow design, automation planning, calculation automation, AI-agent orchestration, MCP integrations, and GitHub implementation.
---

# NAVARIS Master Workflow Skill

## Objective
Turn verified business needs into qualified commercial action and cash. Primary KPI: **CASH COLLECTED**.

## Required evidence chain
FACT → SOURCE → CALCULATION → ASSUMPTION → INTERPRETATION → RISK → ACTION.

Never label an assumption or unverified result as a fact. Record source URLs, source dates, retrieval dates, units, currencies, periods, and confidence/limitations.

## Workflow
1. Discover a company, buyer need, tender, supplier opportunity, project, or market signal.
2. Verify evidence and source quality. If evidence is insufficient, return HOLD and specify one verification action.
3. Analyze relevant financial, operational, market, supplier, and risk information.
4. Run deterministic calculations with input validation, formula/version tracking, and explicit assumptions.
5. Detect and describe a specific commercial opportunity.
6. Qualify need, ability/willingness to pay, decision-maker access, delivery feasibility, risk, and cash path.
7. Prepare a scoped offer/deal plan with deliverables, cost basis, payment terms, and next action.
8. Require human approval before any external message, RFQ/tender, quotation, contract, purchase, investment, or other commercial commitment.
9. Track execution, invoices, receivables, cash received, and outstanding balances separately.
10. Review ROI, conversion, cycle time, margin, and cash collected; loop back, revise, or stop.

## Status contract
Every run ends with exactly one of:
- **GO** — evidence and commercial path support the next approved action.
- **HOLD** — a required fact, validation, approval, or condition is missing.
- **KILL** — a defined criterion fails or no defensible commercial path exists.

Every run records exactly one next action.

## Calculation automation rules
- Use deterministic formulas/code for numeric outputs; AI may explain but must not fabricate calculations.
- Validate missing values, units, currency, period alignment, zero/negative denominators, and source consistency.
- Keep original reported values separate from normalized values and assumptions.
- Do not infer ability to pay or willingness to buy consulting solely from losses or expense ratios.
- Distinguish contracted revenue, invoiced revenue, receivables, and cash actually collected.

## Agent roles
Discovery, Evidence Verification, Financial Analysis, Deterministic Calculation, Opportunity Qualification, Decision-Maker Research, Offer Drafting, Execution/Cash Tracking, and QA/Audit. Agents may research, analyze, and draft; humans approve external commitments.

## MCP and plugin governance
Before adding an MCP server or plugin, verify repository/source, maintainer activity, license, dependencies, permissions, secrets handling, data exposure, operating cost, deployment model, and manual fallback. Do not install or deploy unreviewed code into production.

## Ask the owner when
A missing decision materially changes scope, cost, risk, credentials, privacy, production deployment, or external commitments. State the blocked decision, known/unknown facts, recommended default, options/consequences, and whether safe work can continue. Use reversible defaults for cosmetic decisions.

## GitHub safety
Never commit secrets or private client/deal data. Use synthetic data for tests. Validate Mermaid in GitHub preview. Do not describe a documented workflow as running/deployed until execution and tests prove it.

## Canonical documentation
See [NAVARIS Master Workflow](../../docs/workflows/NAVARIS_MASTER_WORKFLOW.md) for the detailed diagram, controls, formulas, validation checklist, and references.
