---
name: iso-audit
description: "ISO 9001 internal-audit planning and evidence completeness. Use for audit checklists and corrective actions; do not claim certification."
---
# iso-audit Skill

## When to use
ISO 9001 internal-audit planning and evidence completeness. Use for audit checklists and corrective actions; do not claim certification.

## Instructions
1. Discover scope, decision, period, currency, jurisdiction, input files and provenance.
2. Activate the matching toolkit Introduction.md, Guide.md and Standards.md; verify source domain and edition.
3. Validate inputs, then run `python scripts/iso_audit.py` with explicit values. For PDF work, use pdfplumber for extraction and reportlab for reports only if installed; cite source page and flag extraction uncertainty.
4. Separate source facts, calculations, assumptions, interpretation and action. Do not create output from missing inputs.
5. Preserve test evidence and state limitations; obtain human approval before external delivery.

## Bundled scripts, assets, references
- scripts/iso_audit.py: executable helper.
- assets/README.md: input conventions.
- references/README.md: source register requirements.
- Toolkit: toolkit/iso-audit/

## Testability — Tested vs Proposed
Code is implemented but this commit has not run a repository test suite. Status PROPOSED / NOT RUN. Verify source editions, pages, access rights, and validity domain before client use.

## Definition of Done
Inputs traceable; calculation executed against known case; report cites sources/pages, date, units and limitations; no invented data; human reviewer accepts output.
