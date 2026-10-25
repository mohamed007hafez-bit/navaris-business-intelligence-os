---
name: hotel-energy
description: "Hotel and energy-logistics corporate-rate scenarios and commission reconciliation. Use for Borg El Arab, El Max, Adabiya and Sokhna; verify rates directly."
---
# hotel-energy Skill

## When to use
Hotel and energy-logistics corporate-rate scenarios and commission reconciliation. Use for Borg El Arab, El Max, Adabiya and Sokhna; verify rates directly.

## Instructions
1. Discover scope, decision, period, currency, jurisdiction, input files and provenance.
2. Activate the matching toolkit Introduction.md, Guide.md and Standards.md; verify source domain and edition.
3. Validate inputs, then run `python scripts/hotel_energy.py` with explicit values. For PDF work, use pdfplumber for extraction and reportlab for reports only if installed; cite source page and flag extraction uncertainty.
4. Separate source facts, calculations, assumptions, interpretation and action. Do not create output from missing inputs.
5. Preserve test evidence and state limitations; obtain human approval before external delivery.

## Bundled scripts, assets, references
- scripts/hotel_energy.py: executable helper.
- assets/README.md: input conventions.
- references/README.md: source register requirements.
- Toolkit: toolkit/hotel-energy/

## Testability — Tested vs Proposed
Code is implemented but this commit has not run a repository test suite. Status PROPOSED / NOT RUN. Verify source editions, pages, access rights, and validity domain before client use.

## Definition of Done
Inputs traceable; calculation executed against known case; report cites sources/pages, date, units and limitations; no invented data; human reviewer accepts output.
