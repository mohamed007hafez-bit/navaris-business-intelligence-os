# NAVARIS GitHub Automation Catalog — v1

Research date: 2026-10-21
Purpose: shortlist open-source projects for low-cost NAVARIS implementation. This is a candidate catalog, not proof that every project is installed or production-ready. Stars and update cadence change; verify current activity, license, security notices, and requirements before adoption.

## Executive recommendation

Build the first useful workflow with n8n + a small Python reporting module + GitHub Actions. Treat CrewAI as optional orchestration only after the simpler workflow is reliable. Keep the public NAVARIS website static and separate from private customer/financial data.

## Category 1 — Cash flow & services: leads, financial reports, follow-up, invoices

| Candidate | GitHub | Best use | Integration path | Caveat |
|---|---|---|---|---|
| n8n | https://github.com/n8n-io/n8n | Lead capture, CRM updates, scheduled follow-up queues, email/API workflows and reminders | Self-host with Docker; create triggers and HTTP Request nodes; store credentials in the credentials vault | Fair-code license; check terms for intended use |
| ERPNext | https://github.com/frappe/erpnext | Customers, quotations, sales orders, invoices, receivables, accounting and cash-flow reports | Deploy in a secured instance; configure accounts and customers; import reconciled records | Larger setup and accounting configuration |
| CrewAI | https://github.com/crewAIInc/crewAI | Custom research/qualification agents and report drafting | Python environment; define approved source-retrieval and calculation tools; add source ledger and human review | Framework, not a turnkey CRM/accounting system |

Optional invoicing alternative: Invoice Ninja https://github.com/invoiceninja/invoiceninja — invoices, quotes, billing, payment tracking and API integrations. Review current Elastic License 2.0/source-available terms before use. An invoice status is not proof of payment.

NAVARIS cash controls:
- Lead/opportunity value is pipeline, not revenue or collected cash.
- Invoice status and payment status must be separate.
- NAVARIS cash collected remains 0 unless a receipt/payment record is verified.
- Every tender, need signal, rate, volume and contact route must have a direct source and checked date.
- Customer follow-up remains draft-only until Dr. Hafez approves sending.

## Category 2 — Free website design and GitHub Pages

| Candidate | GitHub | Best use | Integration path | Caveat |
|---|---|---|---|---|
| Jekyll | https://github.com/jekyll/jekyll | Native GitHub Pages-friendly static site and Markdown content | Add config, choose Pages publishing source, build and deploy | Ruby toolchain; unnecessary migration if current static HTML works |
| Hugo | https://github.com/gohugoio/hugo | Fast static site with content sections, multilingual pages and themes | Install Hugo in GitHub Actions, build static output and deploy Pages artifact | Requires build workflow/theme migration |
| Astro | https://github.com/withastro/astro | Component-driven static site and high-performance pages | Configure static output and Pages base path; build with Node.js and deploy | More setup than plain HTML |

NAVARIS recommendation: do not migrate the current site just to use a generator. First confirm the existing root index.html and Pages settings. If the current static site works, keep it and add Actions only for repeatable validation/deployment. GitHub Pages is available for public repositories on GitHub Free; private-repository Pages availability depends on plan. Custom domains require repository Pages settings and DNS records; DNS propagation can take up to 24 hours.

Official custom-domain guide: https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site/managing-a-custom-domain-for-your-github-pages-site

## Category 3 — Platform development, dashboards and carrier APIs

| Candidate | GitHub | Best use | Integration path | Caveat |
|---|---|---|---|---|
| Streamlit | https://github.com/streamlit/streamlit | Internal dashboard for leads, deals, invoices, receivables and cash-flow charts | Build Python app; read approved CSV/XLSX/database data; deploy to an approved host | GitHub Pages alone cannot run a Python server app |
| Plotly Dash | https://github.com/plotly/dash | Customized interactive operational and financial dashboards | Build a Python Dash app with Plotly charts and filters; host on a Python-capable server | Requires server hosting |
| n8n | https://github.com/n8n-io/n8n | API/workflow integration for carrier status, email alerts, lead records and reports | Use HTTP Request nodes with carrier APIs; map fields to a normalized shipment schema; schedule polling within API terms | DHL/Maersk API access, credentials, product eligibility and rate limits must be confirmed |

DHL/Maersk integration pattern:
1. Register for relevant official carrier API access and obtain authorized credentials.
2. Start with a sandbox/test account if offered.
3. Map shipment IDs and status timestamps to one normalized schema.
4. Record source, retrieval time, API response code and last successful sync.
5. Add retries with backoff, rate limits, timeouts and alerting.
6. Never fabricate tracking events or place API keys in client-side JavaScript/public repositories.

No DHL or Maersk API was connected by this catalog.

## Category 4 — NAVARIS OS: CI/CD, errors, alerts and documentation

| Candidate | GitHub | Best use | Integration path | Caveat |
|---|---|---|---|---|
| GitHub Actions Starter Workflows | https://github.com/actions/starter-workflows | Build/test/deploy templates, Pages deployment and scheduled jobs | Copy the smallest matching workflow into .github/workflows; use least-privilege permissions; test on a feature branch | Templates need adaptation to this repository |
| Renovate | https://github.com/renovatebot/renovate | Dependency update PRs and dependency maintenance | Configure renovate.json; start with grouped, non-auto-merged PRs; run tests before merging | Avoid auto-merging production dependencies before checks/rollback are proven |
| Sentry | https://github.com/getsentry/sentry | Application error reporting and performance monitoring | Add SDK to a hosted Python/Node service; store DSN in server secrets; route alerts to a monitored channel | Self-hosting is operationally heavy; useful only for a server-side app |

Minimum CI/CD gate:
- Validate HTML/links and run tests for calculation/reporting modules.
- Build the site before deploy; fail visibly if build fails.
- Use idempotency keys and deduplication to prevent duplicate reports/emails.
- Add bounded retries, clear failure logs and owner-visible alerts.
- Keep secrets in GitHub Actions secrets or a secret manager, never committed.
- Generate docs from source/config where practical; review official brand copy changes.

## Implementation sequence

### Phase 0 — Inventory
Inspect main, the existing feature branch, file tree, Pages configuration, current Actions, scheduled jobs and report logic. Do not overwrite working files based on assumptions.

### Phase 1 — Fast, low-risk wins
1. Add a CI workflow on a feature branch for HTML/build checks and existing pricing-engine tests.
2. Add a source-validated lead tracker: company, need, evidence URL, source date, contact route, status, next action, confidence and last checked.
3. Add deterministic invoice/receivable/cash-flow calculations using user-approved data.
4. Generate follow-up drafts and a review queue only.

### Phase 2 — Integrations
1. Pilot n8n in a sandbox with dummy data.
2. Test one carrier API read-only with authorized credentials.
3. Add an internal Streamlit dashboard only if private hosting and access control are available.
4. Consider ERPNext only if workload justifies a full accounting/CRM instance.

### Phase 3 — Release
- Run tests and review security/licensing.
- Open a pull request and inspect the diff.
- Merge only after explicit approval.
- Verify deployment, scheduled run, alert path and rollback.

## Time-saving hypotheses (targets to measure, not guaranteed results)

| Workflow | Initial target | Measurement |
|---|---:|---|
| Lead research and qualification | 30–60% less manual research time | Median minutes per verified lead before/after |
| Invoice/receivables tracking | 30–50% less admin time | Minutes per invoice/payment status update |
| Periodic financial reporting | 40–70% less preparation time | Hours per report and reconciliation exceptions |
| Customer follow-up preparation | 30–60% less admin time | Minutes per opportunity/week; approved drafts count |
| Site build/deploy and regression checks | 50–80% less manual release work | Minutes per release and failures caught before deployment |
| Carrier status reconciliation | 20–50% less manual lookup time | Minutes per shipment and unresolved API exceptions |

These are pilot targets only. Establish a two-week baseline and compare actual logs. Time saved does not imply revenue uplift, shipment volume or cash collected.

## Security and approval policy
- No external outreach, bids, offers, payments or commercial commitments without explicit approval.
- No secret keys, private customer records or finance files in public GitHub Pages.
- Never claim a tender is active, shipment repeats, or invoice is paid without direct evidence.
- Keep audit logs with timestamps, source URLs and action outcomes.
- Stop automation on repeated failures, unexpected API responses or duplicate-send risk.

## Sources
- n8n: https://github.com/n8n-io/n8n
- ERPNext: https://github.com/frappe/erpnext
- CrewAI: https://github.com/crewAIInc/crewAI
- Invoice Ninja: https://github.com/invoiceninja/invoiceninja
- Jekyll: https://github.com/jekyll/jekyll
- Hugo: https://github.com/gohugoio/hugo
- Astro: https://github.com/withastro/astro
- Streamlit: https://github.com/streamlit/streamlit
- Dash: https://github.com/plotly/dash
- GitHub Actions starter workflows: https://github.com/actions/starter-workflows
- Renovate: https://github.com/renovatebot/renovate
- Sentry: https://github.com/getsentry/sentry
