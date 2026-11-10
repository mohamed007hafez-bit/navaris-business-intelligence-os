# NAVARIS project delivery workspace — local MVP

This feature is a founder-operated, browser-local prototype, not a secure client portal.

## Routes

- `/projects` — create and filter project workspaces.
- `/projects/{id}` — project charter, WBS tasks, RAID log, and stakeholder map.
- `/tasks` — standalone local to-do list.

Project records use one validated Local Storage key: `navaris-projects-v1`. Each browser/device keeps its own data. There is no server synchronization, account authentication, access control, encryption, or backup. Use synthetic data only. Clearing browser storage can delete this prototype data.

The project workspace uses generic project-delivery artifact concepts. It does not import template files from the third-party Project Management Playbook repository; inspect its exact artifacts and license before copying any materials.

## Development check

From `app/`, run `npm install`, `npm run build`, then `npm run dev`. No build or browser test is claimed by this document; run these checks in the target environment before relying on the feature.

## Next gate

Replace Local Storage with authenticated, server-side persistence and tenant-scoped authorization only after selecting the production database, threat model, backup/retention policy, and deployment target. Do not expose confidential client records before that gate passes.
