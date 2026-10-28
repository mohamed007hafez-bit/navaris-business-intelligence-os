# NAVARIS Deduplication & Purge Register
**Audit date:** 2026-10-28 | **Branch audited:** main | **Audited tree SHA:** cba757672fbe199f0ecb75e72847a43842e6e222
**Scope:** repository tree and selected workflow, sales, cash-ledger and agent files. This is a repository audit, not a scan of every email, WhatsApp account, cloud drive or external channel.

## Audit summary
- 257 paths matching source/config/document extensions were found in the repository tree.
- 18 GitHub Actions workflow files were found under `.github/workflows/`.
- Multiple similarly purposed workflow files, two WhatsApp sales playbooks, two cash-ledger JSON schemas and a case-variant HTML page were observed.
- No destructive bulk deletion is authorized by this register. Legacy records are preserved until dependency and data reconciliation checks pass.

## Canonical source-of-truth map
| Domain | Canonical source | Legacy/overlap | Decision |
|---|---|---|---|
| Marketing website | `index.html` | `Index.html` | lowercase file is canonical; archive case variant after checking references |
| WhatsApp commercial playbook | `sales-agent-whatsapp.md` | `agents/whatsapp-sales-agent.md`, `templates/outreach/whatsapp-manual.md` | one master claims/guardrails; channel drafts inherit it; retain manual prospect-specific copy separately |
| Cash ledger schema | `data/cash-collected.json` | `docs/cash-collected.json` | canonical is data schema; legacy file is empty and schema-different; do not append new records; reconcile before migration |
| Supplier qualification | `docs/suppliers-qualified.json` | any copied supplier lists | canonical register; qualification requires all defined gates and evidence |
| Core deterministic agents | `agents/{shipping,oilfield,financial,router,config,database}.py` | `navaris_agents/` advanced toolkit | keep separate until packaging and API dependency maps confirm whether they are different product surfaces |
| Windows installer workflow | `.github/workflows/build-desktop.yml` | `desktop-build.yml`, `windows-build.yml`, `navaris-desktop-build.yml`, `navaris-core-only.yml` | overlapping labels, but not all equivalent: root vs `desktop/` project, `npm run dist:win` vs `npm run dist`; do not delete solely by name |
| Pages deployment | `deploy-pages.yml` or `navaris-pages.yml` after explicit selection | both deploy Pages using upload/deploy actions | choose one canonical workflow after comparing intended artifact contents and current Pages settings |
| Quality gate | `navaris-quality.yml` after correcting checks | `navaris-quality-gate.yml` | legacy gate requires founder image and masks build failures with `|| echo`; incompatible with current core-only scope and should be retired |
| Cash-first integrity | `navaris-cash-flow-engine.yml` | `main.yml`, `navaris-toolkit-ci.yml`, other scheduled jobs | compare jobs and test coverage before consolidating; preserve unique workbook/test jobs |
| PDF training | `pdf-auto-train.yml` or `pdf-train.yml` only after comparison | both appear training-related | do not run two training workflows against same inputs without a documented difference |

## Duplicate content and data risks
1. **Repeated sales prompts:** “choose a meeting time?” and “send authorization now?” are push-oriented and do not fit the authority-first strategy. Retire as default openers. Use one evidence-led inbound response and a one-question qualification sequence.
2. **Unverified commercial figures:** EGP 75,000/month, EGP 1.175M LTV, EGP 135K/95K, 50% advance, $1.7M, $4.7B and other pipeline numbers appear as planning assumptions in playbooks or dashboards. These are not approved external claims until sourced and reviewed.
3. **Cash schemas:** two JSON files both represent cash collected but use different fields and policies. The records are currently empty in the inspected copies; do not merge by file name alone.
4. **Case-variant page:** `Index.html` is a second root HTML document; GitHub Pages serves lowercase `index.html` as the canonical index. Treat the case variant as archival, not deployable.
5. **Workflow triggers:** overlapping push triggers can duplicate builds, deploys and quality checks. A name-level count does not prove identical behavior; compare trigger paths, working directory, build command, artifact name and deployment target.

## Purge protocol
- Compute exact-content hashes and normalized-name matches.
- Search code/config/docs for references before retiring a path.
- Reconcile JSON schemas and record counts before migration.
- Move retired assets to `docs/archive/retired-duplicates/` with original path, SHA, reason and date; then remove active duplicate only when safe.
- Never purge bank evidence, signed agreements, audit trails, source evidence or user-owned source files solely because values look similar.
- Do not delete external emails or WhatsApp conversations automatically. This audit did not access those systems.
- Run tests and inspect workflow triggers after each retirement. If a workflow uniquely deploys or builds an intended product surface, preserve it.

## Required follow-up checks
- Verify all `index.html` / `Index.html` references.
- Search for references to `docs/cash-collected.json` and `agents/whatsapp-sales-agent.md`.
- Compare all 18 workflow triggers and artifact outputs; choose canonical Pages and desktop build paths.
- Reconcile every opportunity and supplier by stable ID and legal entity/domain, retaining provenance and last-verified date.
- Review email/WhatsApp channel history only through authorized connectors; deduplicate drafts by normalized subject/body hash, not by recipient alone.

## Completed safe retirements — 2026-10-28
These active duplicates were archived with their original content and blob SHA before removal from active paths:
- `.github/workflows/desktop-build.yml` → `docs/archive/retired-workflows/desktop-build.yml` (overlapping root Windows build).
- `.github/workflows/windows-build.yml` → `docs/archive/retired-workflows/windows-build.yml` (overlapping root Windows build; `build-desktop.yml` retains SHA-256 reporting).
- `.github/workflows/navaris-quality-gate.yml` → `docs/archive/retired-workflows/navaris-quality-gate.yml` (founder-image dependency incompatible with core-only scope and build failure masking).
- `Index.html` → `docs/archive/legacy-site/Index.html` (case-variant duplicate; lowercase `index.html` is canonical).
- `docs/cash-collected.json` → `docs/archive/legacy-data/cash-collected.json` (empty legacy schema; canonical ledger is `data/cash-collected.json`).
- `agents/whatsapp-sales-agent.md` was converted to a short compatibility pointer to `sales-agent-whatsapp.md`, removing duplicate copy while preserving the path for consumers.

The archived originals are retained for rollback/audit. Three workflow files were removed from the active workflow directory; verify the resulting workflow count and all Actions runs before further consolidation. No email or WhatsApp history was deleted because those external channels were not in scope of the accessible repository audit.
