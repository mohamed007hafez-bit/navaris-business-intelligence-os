# NAVARIS AI Agent Implementation Plan

Status: foundation specification only; no autonomous execution is enabled by this document.

## Objective

Build a low-cost, evidence-first agent layer for NAVARIS Business Operations & Development, prioritizing:
1. B2B lead research and qualification.
2. Financial reporting and cash-flow visibility.
3. Human-approved customer follow-up.

## Recommended open-source components

| Capability | Candidate | Role | Integration decision |
|---|---|---|---|
| Lead discovery and sales CRM | https://github.com/asiifdev/business-leads-ai-automation | Prospect capture, qualification, message drafts, CRM pipeline | Evaluate in isolated test environment; check AGPL obligations and Egypt data-source coverage before adoption. |
| Agent orchestration | https://github.com/crewAIInc/crewAI | Coordinate research, validation, calculations, and report writing | Use as an optional Python orchestration layer only after defining tool permissions and deterministic calculations. |
| Customer follow-up | https://github.com/melgarafael/DeskcommCRM | WhatsApp CRM, AI-assisted qualification, follow-up queue and human handoff | Evaluate license, WhatsApp channel terms, hosting and security before production use. |

## NAVARIS agent roles

### Agent A — Lead Intelligence
- Target: petroleum operators, oilfield service providers, freight forwarders, suppliers and industrial buyers.
- Output per lead: company, need signal, source URL, source date, geography, public contact route, fit rationale, confidence, next action.
- Never infer that a company has an active tender or repeat freight unless a dated source supports it.
- Deduplicate by normalized company name + domain.
- Do not send outreach; prepare drafts for human review.

### Agent B — Financial Reporting
- Inputs: user-provided workbook/CSV and approved financial records.
- Compute totals, P&L, cash flow, receivables, payables, margin and plan-vs-actual with deterministic code first.
- AI may explain results, but must not replace formulas or invent missing figures.
- Missing evidence stays blank/unknown; NAVARIS cash collected remains 0 unless receipt evidence is supplied.
- Produce a source ledger and reconciliation exceptions.

### Agent C — Customer Follow-up
- Track each opportunity stage, last contact date, next action date, reply status and owner.
- Draft follow-up messages based on verified CRM history.
- Enforce a human approval gate before sending any email or WhatsApp message.
- Respect opt-outs and rate limits; log every approved send and provider response.

### Agent D — Evidence and Safety Gate
Every material claim must be tagged as FACT, SOURCE, CALCULATION, ASSUMPTION or INTERPRETATION.
Reject unsupported rates, shipment volumes, tenders, contact details, contracts and cash receipts.
Block external sends, bids, offers, or commercial commitments unless explicitly approved.

## Integration sequence

1. Inventory the existing NAVARIS repo, workflows, scheduled jobs, data formats and secrets before adding runtime dependencies.
2. Create a sandbox branch and isolated environment; do not connect a live WhatsApp number or production mailbox during initial tests.
3. Prototype Lead Intelligence against a small manually reviewed sample of public companies.
4. Prototype Financial Reporting using synthetic/sample data, then reconcile against a user-approved workbook.
5. Prototype Follow-up in draft-only mode; verify opt-out handling, deduplication and approval gates.
6. Add scheduling only after the test suite passes; store secrets in environment variables or GitHub Actions secrets, never in source files.
7. Enable one narrow production workflow at a time and retain logs, rollback instructions and a kill switch.

## Acceptance criteria

- Every lead has a direct source URL and source date, or is marked unverified.
- Duplicate leads are flagged rather than silently re-created.
- Financial calculations reconcile to source records and include a calculation trail.
- No external message is sent without a recorded approval.
- Failed runs are logged and cannot trigger duplicate reports or messages.
- Secrets are not committed; logs do not expose credentials or unnecessary personal data.

## Time-saving hypothesis (pilot estimates, not guarantees)

| Workflow | Baseline to measure | Initial target after validation |
|---|---|---|
| Lead research and qualification | Median manual minutes per verified lead | 30–60% less research time |
| Recurring financial report | Manual preparation and reconciliation hours per report | 40–70% less preparation time |
| Follow-up preparation and queue review | Minutes per opportunity per week | 30–60% less administrative time |

Measure these against a 2-week baseline. Do not claim revenue uplift or cash collected from time saved alone.

## Deployment prerequisites

- Confirmed Python/Node versions and existing application architecture.
- Approved model/API provider and budget cap.
- Approved data sources and storage/retention rules.
- Separate test mailbox/WhatsApp channel for end-to-end validation.
- A human owner for approval queues and exception handling.

## Important limitation

This file defines the implementation path. It does not install the external projects, provision infrastructure, connect credentials, or enable autonomous execution. Production activation requires repository inspection, dependency review, tests, and explicit approval of external communication channels.
