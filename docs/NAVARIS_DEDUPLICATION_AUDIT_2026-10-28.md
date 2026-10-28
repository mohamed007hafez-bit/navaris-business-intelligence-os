# NAVARIS Repository De-duplication Audit — Baseline
Date: 2026-10-28
Branch: main
Commit inspected: cba757672fbe199f0ecb75e72847a43842e6e222
Method: recursive Git tree inventory plus targeted review of workflow definitions and core agent files. This is a static baseline scan, not a scan of external email accounts or all files in the personal Library.

## Inventory snapshot
- 317 repository files found in recursive tree response.
- Two root-level HTML candidates with case variation: `index.html` and `Index.html`. GitHub Pages is case-sensitive; keep `index.html` as canonical, compare content/history and inbound links before archiving the other.
- 18 files under `.github/workflows/`.
- Potentially overlapping workflow groups identified below.
- At least two separate outreach/template locations: `agents/whatsapp-sales-agent.md`, `sales-agent-whatsapp.md`, `templates/outreach/whatsapp-manual.md`, `data/outreach/2026-10-06-consulting-investment.md`, and `scripts/auto-outreach.js`. These are candidates for semantic review, not proven exact duplicates.
- Two tender-monitoring state/artifact paths appear: `data/seen_tenders.json` and tender-report logic in `navaris_report.py` / `docs/NAVARIS_HYBRID_TENDER_ENGINE.md`. Confirm shared identifiers and idempotency before merging.

## Workflow overlap candidates
| Purpose | Files | Recommended canonical choice | Safe disposition |
|---|---|---|---|
| GitHub Pages | `.github/workflows/navaris-pages.yml`, `.github/workflows/deploy-pages.yml` | `navaris-pages.yml` as minimal site publisher after verifying live Pages settings | Disable/delete the other only after confirming it is not required for assets/PWA and the chosen deployment is green |
| Quality gate | `.github/workflows/navaris-quality.yml`, `.github/workflows/navaris-quality-gate.yml` | One consolidated gate, with exact title, JSON, tests and truthful asset checks | Current gate scripts have materially different checks; consolidate, do not blindly delete |
| Desktop packaging | `build-desktop.yml`, `desktop-build.yml`, `navaris-desktop-build.yml`, `navaris-core-only.yml`, `windows-build.yml` | Keep core-only build as canonical for core installer; separately document any production/legacy packaging need | Compare triggers, artifacts and package targets before retiring four candidates |
| PDF source processing | `pdf-auto-train.yml`, `pdf-train.yml` | One source validation/index pipeline; real training/embedding separate and opt-in | These workflows validate different catalogue structures (9 vs 38 agents), so they are not safely interchangeable yet |
| Main OS / daily reporting | `main.yml`, `navaris-cash-flow-engine.yml`, `navaris-daily-report.yml`, `night-shift.yml`, `navaris-toolkit-ci.yml` | Assign one owner per distinct purpose, share common reusable tests | Do not remove until triggers, side effects, email, and artifact outputs are mapped |

## Confirmed architecture conflicts / risks
1. Root HTML case variant exists. The canonical public path should be lowercase `index.html`; archive the other only after content comparison.
2. `navaris-pages.yml` publishes a minimal site from `index.html`; `deploy-pages.yml` publishes the repository root. Competing Pages deployments can publish different artifact contents.
3. `navaris-quality.yml` requires `manifest.json`, `service-worker.js`, `navaris-exe/package.json`, `app/package.json`, and `toolkit/index.json`; other workflows target a different core-only surface. Quality policy must match the intended current product, not stale files.
4. `navaris-quality-gate.yml` fails if founder image is missing and uses a non-fatal build command (`npm run build || echo ...`), which can misrepresent build status. Founder presence should be a deliberate product requirement, not an incidental CI gate.
5. `pdf-auto-train.yml` and `pdf-train.yml` assume different `agents.json` schemas and different agent counts. This is a configuration conflict until reconciled.
6. The core `agents/database.py` explicitly documents SQLite as unencrypted placeholder; it must not store confidential client/bank evidence.
7. The core `agents/router.py` dispatches shipping/oilfield/financial analysis but has no implemented bank-receipt verification, verified match state, or SLA approval gate at this baseline.

## Purge decision and action taken
- Removed `.github/workflows/deploy-pages.yml` in commit `16d5f4d8ccb3f3af460d4c02de0c43f9aacf9fe5`. It published the entire repository root while `navaris-pages.yml` builds a minimal `_site` artifact from the canonical `index.html`; the competing publisher could expose unrelated repository files and create inconsistent deployments. `navaris-pages.yml` remains the intended publisher.
- No other files were deleted in this pass. Similar filenames or overlapping purpose are not proof of duplicate content. Use a content hash + semantic comparison + trigger/side-effect review, preserve provenance, and retire one workflow at a time after the replacement passes.
- External email channels were not inspected; no email or CRM records were purged.
- `Index.html` and `index.html` are both present but differ in content/size. `index.html` remains the canonical public path; `Index.html` is not deleted until its unique content/history is reviewed.

## Required next audit
- Compute SHA-256 for every repository blob and exact duplicate groups.
- Compare `Index.html` and `index.html` content.
- Export workflow trigger, write permissions, secrets, side effects, and artifact names into one registry.
- Search outreach content for repeated copy, audience, CTA, and sequence steps; approve one canonical template per segment.
- Review personal Library and connected email/CRM separately through authorized tools; this repo scan cannot claim coverage of those sources.
