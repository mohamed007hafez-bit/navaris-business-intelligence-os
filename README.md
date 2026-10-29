# NAVARIS Business Intelligence OS

NAVARIS uses a canonical cash-first control layer, a published web gateway, and separate domain/desktop components. This repository preserves the existing local workbook and Electron workflows while centralizing the governing financial formulas and evidence rules.

## Canonical system of record

- `navaris_core_engine.py` — single canonical registry for the nine service verticals, five coordinating agent roles, OER, operating margin, the illustrative 15% intermediary commission, and the fail-closed cash-recognition rule.
- `NAVARIS_CORE_MASTER_LOG.md` — operating doctrine, evidence chain, controls and configuration notes.
- `index.html` — canonical GitHub Pages website entry point. Its title is intentionally `NAVARIS GATEWAY EGYPT`.
- `tests/test_navaris_core_engine.py` — regression tests for canonical formulas and cash gates.
- `scripts/github_sync.py` — optional GitHub Contents API helper. It reads credentials from `NAVARIS_GITHUB_TOKEN`; credentials must never be committed to this repository.

## Locked formula policy

- **Operating Expense Ratio:** `(OPEX / Net Revenue) * 100`
- **Operating Margin:** `(EBIT / Net Revenue) * 100`
- **Cash recognition:** `CASH COLLECTED = 0` until finance independently verifies a bank receipt and reconciles the transaction. Presence of metadata alone is not independent proof.
- **Intermediary commission:** 15% is a planning default only; the fee basis and actual rate require a written agreement.

When net revenue is not positive, ratio functions return `None` rather than manufacturing a percentage. Negative EBIT is allowed.

## Domain components

- `engines/legacy_route_pricing.py` — route costing and editable workbook/chart construction used by the local hybrid CLI. This is a domain module, not the authority for canonical OER, operating margin, commission policy or cash recognition.
- `main.py`, `pricer_agent.py`, `scout_agent.py`, `cash_agent.py` and related root CLI modules — existing local pricing/workbook compatibility path. Retained because they are referenced by current tests and workflows.
- `agents/` and `navaris_agents/` — separate domain/control modules; no legacy module is automatically promoted to evidence-verified cash or execution approval.
- `desktop/`, `app/` and `cross-platform/` — separate application targets; do not treat them as duplicate byte-identical files.

The five coordinating agent roles are registered centrally. Their registry does not imply that external autonomous services, unattended web discovery, or background execution are enabled.

## Quality checks

The active GitHub Actions workflows validate the canonical title, JSON, Python compilation, canonical engine tests, agent/control tests, the secure-sync path validator, and token-like credential patterns. The Windows x64 workflow also builds the Electron installer and uploads the installer and source ZIP artifacts.

For local checks:

```bash
python -m unittest discover -s tests -p 'test_navaris_core_engine.py' -v
python -m unittest discover -s tests -p 'test_github_sync.py' -v
python -m unittest discover -s tests -p 'test_navaris_os.py' -v
npm install
npm run dist
```

For GitHub sync, create a fine-grained token with only the required repository contents permission, set `NAVARIS_GITHUB_TOKEN` in the local environment, and never paste it into source code. Any token previously committed must be revoked even after the offending file is removed.
