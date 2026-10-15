# NAVARIS OS — Local Hybrid Operating Manual

## Purpose

Implement the supplied NAVARIS skill as a small, beginner-operable local Python application that produces an editable Excel workbook with native charts. It is designed for local calculations first and optional cloud eligibility later.

## Architecture

Input JSON / locally verified records
→ scout_agent.py
→ pricer_agent.py → navaris_core.py (fixed formulas)
→ evidence and decision gate
→ ncnda_agent.py (draft only) and cash_agent.py (forecast vs collected)
→ chatgpt_bridge.py (approval policy only; no network call)
→ main.py
→ output/NAVARIS_Agnatics_OS_FINAL.xlsx

## Installation

### Windows
1. Download or clone the repository using the user's existing GitHub workflow or desktop Git client.
2. Install Python 3.10+ (Python 3.12 is used in CI).
3. Run run_navaris_local.bat.
4. Open output/NAVARIS_Agnatics_OS_FINAL.xlsx in Excel.

### macOS / Linux
1. Install Python 3.10+.
2. Run bash run_navaris_local.sh.
3. Open output/NAVARIS_Agnatics_OS_FINAL.xlsx in Excel.

### Manual commands

    python -m pip install -r requirements.txt
    python main.py --demo
    python -m unittest discover -s tests -v

To use a JSON file, copy data/navaris_demo_input.json, replace the sample values with verified records, and run:

    python main.py --input-json data/navaris_demo_input.json

The included JSON is an example template, not a verified commercial opportunity. Maintain source URL, source date, contact, RFQ/model, payment terms, and evidence status in the input record before making a decision.

## Decision and financial controls

- Margin and grade calculations are reproducible and unit-tested.
- The 30/70 split is a model from the supplied skill and must not be treated as an agreed commission without a signed contract.
- Forecasts and projected client counts are separate from actual cash collected.
- Actual cash collected defaults to zero unless receipt evidence is explicitly provided.
- NCNDA generation is draft-only and requires a named counterparty and a high enough grade. Review by qualified counsel and signatures by authorized parties remain required.
- The app does not submit bids, send emails, contact buyers, contact suppliers, or sign agreements.

## Local Hybrid and data security

- The default run is local and makes no web requests.
- chatgpt_bridge.py enforces eligibility only; it does not call an AI service.
- A cloud-eligible decision requires all three: grade ممتاز, the --approve-cloud command-line flag, and environment variable NAVARIS_ALLOW_CLOUD=1. Even then, this application sends no data; a provider adapter would need to be separately implemented and reviewed.
- Never paste secrets into source files or commit them. Keep .env, client data, outputs, logs, and private files outside Git.
- Local processing is not equivalent to automatic encryption. Use OS account permissions and full-disk encryption (e.g., BitLocker/FileVault/LUKS) on any device storing sensitive client information. Back up to a controlled, encrypted location.
- Do not use real personal, financial, or counterparty-sensitive data in the demo.

## GitHub Actions

The NAVARIS Local Hybrid OS — Tests and Workbook workflow checks syntax, runs regression tests, builds the sample workbook, validates required sheets/native charts, and stores the generated workbook as a temporary artifact. It does not discover live tenders, make cloud calls, send messages, or prove the commercial validity of sample data.

## Known boundaries

1. Tender discovery is currently input-driven; it does not automatically scrape or authenticate to procurement portals.
2. Supplier/OEM and buyer qualification still requires source-backed verification.
3. The cloud adapter is not implemented; only the approval gate exists.
4. Financial models do not replace legal, tax, procurement, engineering, or investment advice.
5. Do not treat a high margin grade alone as a GO decision. Check evidence, working capital, counterparty risk, payment terms, compliance, and days-to-cash.
