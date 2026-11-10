# NAVARIS local run and agent readiness

This note describes the current repository state; it is not a production-readiness certification.

## What the client-facing preview does

The Next.js app at `app/` now has a bilingual business-operations landing page and an enquiry form. The form saves a non-sensitive draft in the current browser's `localStorage` only. It does **not** send an enquiry to NAVARIS, synchronize it to another device, or provide a client account. Do not enter confidential, bank, credential, or customer data into this preview.

Run the web preview locally:

```bash
cd app
npm install
npm run dev
```

Then open `http://localhost:3000`. To make it available on another device or publicly, deploy a server and configure authentication, storage, access controls, retention, backups, and appropriate security review first. A local browser draft is not a shared database.

## Do autonomous agents currently work?

**Not as an autonomous multi-agent production system.** The repository contains agent role descriptions and workflow plans. `backend/main.py` exposes deterministic API endpoints for health, discovery, draft proposals, risk calculations, ISO-gap calculations, daily tasks, and closeout checks. Those endpoints are not a running autonomous team that independently researches, decides, stores work, or communicates with clients.

`backend/openai_adapter.py` is an optional server-side adapter. It requires `OPENAI_API_KEY` in the backend environment, and its presence alone does not orchestrate all listed agents. No key is included in the repository. AI-assisted analysis must remain review-gated; external messages and business commitments must not be sent automatically.

To assess and test the current agent/API functionality, first install backend dependencies from the repository's `requirements.txt`, then start the API from the repository root:

```bash
python -m pip install -r requirements.txt
python -m backend.main
```

Check `http://127.0.0.1:8000/health` and the interactive API docs at `http://127.0.0.1:8000/docs`. These checks test the API that exists; they do not prove autonomous-agent readiness. Keep the service bound to localhost for local testing.

## Important implementation and release gaps

- The previous portal screen generated sample client names, financial metrics, currency rates, and source references in the browser. Do not treat those demo values as real evidence or financial analysis; this client-facing preview replaces that mock screen.
- The backend charter has a branding inconsistency with the repository's current NAVARIS identity instructions. Resolve that before release.
- The portal includes Supabase and payment dependencies, but credentials, authentication policies, row-level access rules, and payment processing are not configured as a deployable service.
- The current enquiry form is intentionally local-only. A production intake needs a secure server-side persistence design and a human-reviewed workflow.
- A production release still needs automated tests for the actual app/API, secret and data handling review, deployment configuration, domain and public-claim verification, and founder approval.
- “Like Torrent” is interpreted here as running on your own computer. NAVARIS is not being made into a peer-to-peer file-sharing system; client business records should not be distributed between users' computers.

## Safe launch sequence

1. Test the local landing page and form in a browser.
2. Select a production database and define authenticated roles and access policies.
3. Implement server-side enquiry persistence, evidence references, and an audit log.
4. Add and test deterministic workflows before enabling optional AI assistance.
5. Keep outbound sending disabled until explicit founder approval is implemented and tested.
6. Run acceptance, security, backup/restore, and deployment checks before public launch.
