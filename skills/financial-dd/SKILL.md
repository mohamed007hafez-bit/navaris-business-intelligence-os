---
name: financial-dd
description: "Financial Due Diligence — Altman Z, ROIC, DCF and financial statements. Use for company financial analysis, valuation or distress screening."
---
# financial-dd Skill

## When to use
Financial Due Diligence — Altman Z, ROIC, DCF and financial statements. Use for company financial analysis, valuation or distress screening.

## Instructions
1. Discover scope, decision, period, currency, jurisdiction, input files and provenance.
2. Activate the matching toolkit Introduction.md, Guide.md and Standards.md; verify source domain and edition.
3. Validate inputs, then run `python scripts/financial_dd.py` with explicit values. For PDF work, use pdfplumber for extraction and reportlab for reports only if installed; cite source page and flag extraction uncertainty.
4. Separate source facts, calculations, assumptions, interpretation and action. Do not create output from missing inputs.
5. Preserve test evidence and state limitations; obtain human approval before external delivery.

## Bundled scripts, assets, references
- scripts/financial_dd.py: executable helper.
- assets/README.md: input conventions.
- references/README.md: source register requirements.
- Toolkit: toolkit/financial-diagnosis/

## Testability — Tested vs Proposed
Code is implemented but this commit has not run a repository test suite. Status PROPOSED / NOT RUN. Verify source editions, pages, access rights, and validity domain before client use.

## Definition of Done
Inputs traceable; calculation executed against known case; report cites sources/pages, date, units and limitations; no invented data; human reviewer accepts output.
