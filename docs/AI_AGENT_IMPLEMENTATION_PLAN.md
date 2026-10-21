# NAVARIS AI Agent Integration Plan (Single Company — Alexandria)

**Owner:** Dr. Mohamed Hafez Khalifa  
**Repository:** https://github.com/mohamed007hafez-bit/navaris-business-intelligence-os  
**Policy:** NAVARIS only. No second repository. No automatic external sending, bidding, pricing commitments, or client-facing actions without Master approval. Treat all third-party code as untrusted until reviewed.

## Recommended top 3

### 1. OpenOutreach — B2B lead discovery and qualification
- Source: https://github.com/eracle/OpenOutreach
- Purpose: discover B2B prospects from a product/ideal-customer description, qualify them with a reason, and export CSV.
- Fit: highest priority for NAVARIS sales lead generation (petroleum/oilfield suppliers, freight/logistics, industrial buyers in Alexandria/Borg El Arab/El Max/Wardian).
- Runtime: Python 3.12+, CLI. Upstream README describes GPLv3 and requires an LLM provider key plus BetterContact account/key; email enrichment may consume credits. Its current README says it does not send email.
- Safe integration: run separately first; export CSV; pass it through `python integrations/lead_pipeline.py leads.csv`; review and approve any follow-up drafts manually.
- Start: `pip install openoutreach`; `openoutreach init`; configure provider credentials locally; `openoutreach find 10 > leads.csv`. Confirm upstream README and licence before production use.

### 2. n8n — operations orchestration and customer follow-up workflows
- Source: https://github.com/n8n-io/n8n
- Purpose: connect schedules, inbox/CRM/spreadsheets, webhooks and approved actions in visual workflows.
- Fit: route new leads into a review queue, remind NAVARIS to follow up, create daily reports, and add a human approval step before outbound messages.
- Runtime: TypeScript-based workflow automation platform; self-hosting has deployment and maintenance requirements. Review current licence/edition terms before commercial deployment.
- Safe integration: deploy locally or on a controlled server; start with CSV/Sheets/CRM intake → deduplication → task/reminder → draft creation → human approval. Keep send nodes disabled until explicitly approved.

### 3. Anthropic Financial Services reference agents — financial research/reporting patterns
- Source: https://github.com/anthropics/financial-services
- Purpose: reference workflows, skills and data connectors for financial research, investment banking and private-equity workflows.
- Fit: adapt analytical structure for NAVARIS financial reporting and opportunity screening; do not assume it is a drop-in local finance agent.
- Runtime/cost: check current upstream README, licence, model/API requirements, and deployment path before installation. It may rely on Anthropic services and is not guaranteed to be zero-cost.
- Safe integration: borrow only reviewed patterns; keep NAVARIS reporting deterministic and local, calculating totals from actual CSV/XLSX exports before any LLM narrative.

## Implemented local bridge

`integrations/lead_pipeline.py` is a dependency-free Python CSV bridge for qualified leads. It reads an upstream lead CSV, normalizes columns, deduplicates by email/profile URL/company+name, writes a review CSV and follow-up draft CSV, and marks every draft `DRAFT_ONLY_REQUIRES_MASTER_APPROVAL`. It does **not** send email, scrape websites, purchase contact data, or call a paid API.

Run: `python integrations/lead_pipeline.py leads.csv`

Outputs next to the input CSV: `navaris_leads_review.csv` and `navaris_followup_drafts.csv`.

## Rollout sequence

**Phase 1 — Sales (same day after local environment/provider setup):**
- Define separate ICPs for petroleum/oilfield suppliers, industrial buyers, and freight/logistics partners.
- Run a small batch (10 leads); verify source, relevance, duplicates, geography, and contact provenance.
- Import only approved rows to the NAVARIS lead register.

**Phase 2 — Finance (1–2 working days after data format is agreed):**
- Define canonical input columns: date, transaction/reference, category, currency, amount, direction, evidence/source.
- Produce cash-in/cash-out, gross commission, receivables ageing, and opportunity-level margin summaries from actual records.
- Unsupported cash remains 0; label assumptions explicitly. Never generate fictional financial data.

**Phase 3 — Follow-up operations (1 working day after mail/CRM connector setup):**
- Add due-date reminders, status changes, and draft generation.
- Require explicit human approval before sending messages, quoting prices, signing commitments, or submitting tenders.
- Maintain opt-out/suppression records and prevent duplicate outreach.

## Expected time savings (planning estimates, not measured results)

| Workflow | Manual baseline assumption | Target after validation | Estimated time saved |
|---|---:|---:|---:|
| Research and qualify 10 prospects | 2–4 hours | 30–60 minutes review | 50–75% |
| Prepare a weekly finance summary | 2–4 hours | 30–90 minutes validation | 50–75% |
| Track follow-ups for 20 open leads | 60–120 minutes/day | 15–30 minutes/day | 50–75% |

These are pilot targets, not verified outcomes. Measure actual cycle time over two weeks before claiming ROI.

## Security and acceptance gates
- Never commit API keys, email passwords, tokens, or customer secrets.
- Use least-privilege credentials and local environment variables/secret manager.
- Verify licence, dependencies, maintenance activity, and upstream security advisories before installing.
- Run a 10-record test first; inspect outputs and back up data.
- No external email is sent automatically. All outreach remains draft-only until approved by the NAVARIS Master.
- Existing NAVARIS single-company / Alexandria structure remains authoritative.
