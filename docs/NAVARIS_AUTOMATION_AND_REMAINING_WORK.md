# NAVARIS: what remains and how to continue without repeated approvals

## Current implemented slice

The development branch contains a bilingual client-facing landing-page preview, a browser-only intake draft (no network submission), and a local deterministic workflow API. The API exposes `/health`, `/agents/status`, and `/workflow/run`. Five workflow roles run when explicitly requested: intake, evidence validation, risk review, strategy planning, and quality review. Outputs remain drafts and external actions are disabled.

Tests for the deterministic workflow can be run from the repository root:

```bash
python -m unittest tests.test_local_workflow -v
```

Run the local API after installing root `requirements.txt`:

```bash
python -m pip install -r requirements.txt
python -m backend.main
```

Open `http://127.0.0.1:8000/docs`; submit a sample request to `/workflow/run`. `/agents/status` clearly reports the current capability and limitations.

## What is not finished

1. Install/run validation on Mohamed's Windows machine: this remote coding session cannot access the D: drive, install programs, or verify its environment.
2. Secure persistence, user authentication, tenant isolation, evidence file storage, backups, retention, and audit history.
3. Production client intake submission, case status workspace, and founder review queue.
4. Agent integrations for document parsing and optional model assistance, with permission, evaluations, cost limits, source handling, and human review.
5. Automated integration/UI tests, dependency pinning, accessibility review, and reliable release pipeline.
6. Deployment, domain, privacy notice, terms, support process, and claim/legal review.
7. Founder acceptance testing and explicit release approval.

## Work policy

Continue implementation autonomously on `docs/navaris-launch-roadmap` for reversible, low-risk code, documentation, tests, and local previews. Do not pause for approval at every small step. Keep changes in the development branch and report checkpoints. Ask before irreversible/high-impact actions: merging to `main`, public deployment, removing legacy content or workflows, enabling customer-data collection, configuring paid services, using credentials, contacting customers, or sending proposals/contracts. Never commit secrets or real customer/bank data.
