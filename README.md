# NAVARIS - Single Company - Alexandria - Dr. Mohamed Hafez Khalifa - One Main

**Company lock:** NAVARIS only; one company based in Alexandria, Egypt. No HAFEZ GROUP, holding company, or other companies.

## One Main architecture
- Dr. Mohamed Hafez Khalifa is the single master.
- `core/master.py` is the only task-assignment authority.
- 13 subordinate agents execute bounded tasks and report to the master; they cannot assign tasks to one another.
- Market: Egypt only in this version.
- Core: Business Doctor + Technical Services, informed by the owner's IOD rigless background (2012–2013).
- Storage: local SQLite. No paid APIs or API keys are needed.

## Install
Python 3.10+ recommended.
```bash
bash install.sh
```
The installer installs `fastapi` and `uvicorn`, then runs the master health check.

## Run local API
```bash
python mcp-server/server.py
```
Health endpoint: `http://127.0.0.1:8000/health`. The service binds to loopback by default.

## Master commands
```bash
python core/master.py health
python core/master.py --health
python core/master.py assign --agent 06 --task "Describe the task"
```
HTTP `POST /tasks` and `POST /reports` require the `X-Navaris-Master-Key` header. Set `NAVARIS_MASTER_KEY` in the server process environment before starting the API. The server fails closed with HTTP 503 if the key is not configured. Never put the key in source code, documentation, browser code, or Git history. The old example key was exposed and must not be reused.

## Safety and limits
- Retry logic is bounded to 10 attempts.
- The orchestrator does not download or modify code automatically.
- This GitHub commit adds source files; it does not install dependencies or start a server on your device.
- Clients and subcontractors remain relationships of NAVARIS, not separate companies.


## Automations and workflows

All repository workflows are in [`.github/workflows/`](.github/workflows/).

| Workflow | Trigger | What it actually does | Boundary |
|---|---|---|---|
| [NAVARIS Website and OS Quality Gate](.github/workflows/navaris-quality-gate.yml) | Push, pull request, manual, daily 00:15 Cairo | Validates the canonical website title/assets, compiles Python/API, runs all tests including API security regressions, builds and checks an Excel workbook. | Does not source live tenders or send outreach. |
| [NAVARIS Local Hybrid OS — Tests and Workbook](.github/workflows/main.yml) | Push, pull request, manual | Runs core regression tests and builds illustrative/demo and AOG quote workbooks. | AOG quote remains unpriced without verified buyer/supplier evidence. |
| [NAVARIS Cash-First Integrity Engine](.github/workflows/navaris-cash-flow-engine.yml) | Daily, manual, selected pushes | Validates cash-first policy, tests the core, and builds the Excel workbook. | Not a live tender scraper and does not verify commercial opportunities. |
| [NAVARIS Daily Petroleum Tender Intelligence](.github/workflows/navaris-daily-report.yml) | Daily 18:00 UTC, manual | Checks public HTML links on GASCO and ENPPI pages, deduplicates candidates, writes a Markdown report, and attempts SMTP email delivery. | Only keyword-based candidate discovery; cannot verify logged-in portals, JavaScript-only pages, PDFs, tender eligibility, or freight demand. Requires the six `MAIL_*` / `REPORT_EMAIL` repository secrets for email delivery. |

### API secret setup

The local API now reads `NAVARIS_MASTER_KEY` from the server process environment. Both `POST /tasks` and `POST /reports` require `X-Navaris-Master-Key`; the API returns HTTP 503 when the secret is not configured. The previous hardcoded example key is compromised and must not be reused. Configure a new, long random key on the machine that runs the API; this is separate from the email secrets above.


## NAVARIS V2 closure notes (2026-10-25)
- Public DNS troubleshooting: on the affected local network only, test DNS resolvers 8.8.8.8 and 1.1.1.1. The reported local address 192.168.1.10 is not a public GitHub Pages DNS target. Do not add it to public DNS records.
- Internal draft documents: [87-checkpoint toolkit](docs/NAVARIS_TOOLKIT_87.md), [ISO profile](docs/NAVARIS_ISO_PROFILE.md), [consulting pricing](docs/NAVARIS_CONSULTING_PRICING.md), and [cash diagnosis](docs/NAVARIS_CASH_DIAGNOSIS.md).
- All pricing is draft until approved; cash remains zero absent documentary receipt evidence.
