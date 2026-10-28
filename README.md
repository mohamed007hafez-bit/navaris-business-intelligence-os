# NAVARIS Business Intelligence OS — Core Only

Minimal offline-first starter with three deterministic Python agents, router, configuration, local SQLite placeholder, Electron desktop shell, and a marketing-only Three.js landing page.

## Included
- agents/shipping.py: landed-cost calculations from explicitly supplied figures only.
- agents/oilfield.py: oilfield requirement qualification checklist.
- agents/financial.py: current ratio, working capital, and EBITDA margin.
- agents/router.py: JSON request router and CLI.
- agents/config.py and agents/database.py: local paths and SQLite history placeholder.\n- agents/controls.py: bank-reconciliation, demand/supply evidence, and SLA-readiness gates. These validate record completeness; they do not independently authenticate evidence.
- main.js and package.json: Electron desktop shell and Windows x64 NSIS packaging.
- index.html: marketing-only Moths to Light visual using Three.js.
- tests/test_core.py: basic deterministic tests.

## Run
Requires Python 3.10+, Node.js, and npm. Install test dependencies with python -m pip install -r requirements-dev.txt. Run tests with python -m pytest -q. Install desktop dependencies with npm install, then run npm start.

On Windows x64, run npm run dist to build the NSIS installer in release/. Target installer size is 70–80 MiB, but actual size depends on Electron and packaging.

Control examples (JSON payloads are illustrative; do not invent evidence):\n- Cash status: {\"operation\":\"record_cash\",\"payload\":{...}}; status remains PAYMENT_PENDING until finance verification and reconciliation fields are present.\n- Demand/supply: {\"operation\":\"verify_match\",\"payload\":{\"demand\":{...},\"supply\":{...}}}; output is review-only, never execution approval.\n- SLA readiness: {\"operation\":\"activate_sla\",\"payload\":{...}}; no SLA becomes active without signed scope, provider capacity evidence and clock rules.\n\nFor direct agent use, run from repository root with module mode:
python -m agents.router
Then paste a JSON request on stdin, such as {"agent":"shipping","payload":{"freight":100,"customs":20,"handling":5}}.

SQLite is a local, unencrypted placeholder stored at data/navaris_core.sqlite3 by default. Do not store confidential client data until local access controls, backups, and planned SQLCipher/AES protection are implemented and tested. No cloud database, Ollama, encryption proof, or outreach automation is included.
