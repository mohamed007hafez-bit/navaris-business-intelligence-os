# NAVARIS AI Hybrid — Petroleum Tender Intelligence MVP

## Design
1. Deterministic Python collector reads publicly accessible static HTML from GASCO and ENPPI and flags links matching Arabic/English tender keywords.
2. Evidence records preserve company, title, URL, source page and UTC check time. Publication date and closing deadline are not guessed.
3. SHA-256 IDs and `data/seen_tenders.json` suppress repeat notifications.
4. Transparent technical/commercial screening framework; numeric scores are not calculated until the tender's official weights and supplier evidence exist.
5. Master approval is required for qualification decisions, outreach, bids and commercial commitments.
6. GitHub Actions tests, collects, emails, archives reports, and attempts a failure alert.

## Equations and evaluation
- Weighted technical score: `S = sum(w_i * s_i) / sum(w_i)`, only when criteria and weights are supported by tender documents.
- Total landed cost = supply + freight + insurance + customs/tax + inspection + financing + evidence-based risk reserve.
- Contribution margin = verified net revenue − direct variable costs.
- Bid/no-bid gate: mandatory eligibility first, then technical fit, delivery, payment terms, cash exposure, margin and risk.

## Configure email
Add these repository secrets in Settings → Secrets and variables → Actions: `MAIL_SERVER`, `MAIL_PORT` (usually 587), `MAIL_USERNAME`, `MAIL_PASSWORD`, `MAIL_FROM`, `REPORT_EMAIL` (set to `mohamed007hafez@gmail.com`). SMTP STARTTLS and authenticated sending must be enabled by the provider. Never commit credentials.

## Run
Python 3.12+: `python -m unittest discover -s tests -v` then `python navaris_report.py`. Manual run: GitHub → Actions → NAVARIS Daily Petroleum Tender Intelligence → Run workflow.

## Schedule caveat
Workflow cron `0 18 * * *` runs at 18:00 UTC, or 9 PM Cairo while Cairo is UTC+3. During UTC+2, use `0 19 * * *`. GitHub scheduled jobs may be delayed; exact-minute delivery is not guaranteed. Review cron after seasonal time changes.

## Limitations
Static HTML only; no bypass of CAPTCHA/login and no parsing of JS-rendered content or PDFs. Keyword matching can miss results or create false positives. Dates remain unavailable unless verified. Live source compatibility and SMTP delivery must be tested. A failure alert itself depends on working secrets and SMTP. GitHub Actions needs permission to push state to `main`; branch protection may block that step. This is an MVP and makes no unsupported claim of outperforming ChatGPT or Claude.
