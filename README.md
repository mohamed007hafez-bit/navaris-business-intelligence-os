# NAVARIS Business Intelligence OS — Core Only

Minimal offline-first starter with three deterministic Python agents, router, configuration, local SQLite placeholder, Electron desktop shell, and a marketing-only Three.js landing page.

## Included
- agents/shipping.py: landed-cost calculations from explicitly supplied figures only.
- agents/oilfield.py: oilfield requirement qualification checklist.
- agents/financial.py: current ratio, working capital, and EBITDA margin.
- agents/router.py: JSON request router and CLI.
- agents/config.py and agents/database.py: local paths and SQLite history placeholder.
- main.js and package.json: Electron desktop shell and Windows x64 NSIS packaging.
- index.html: marketing-only Moths to Light visual using Three.js.
- tests/test_core.py: basic deterministic tests.

## Run
Requires Python 3.10+, Node.js, and npm. Install test dependencies with python -m pip install -r requirements-dev.txt. Run tests with python -m pytest -q. Install desktop dependencies with npm install, then run npm start.

On Windows x64, run npm run dist to build the NSIS installer in release/. Target installer size is 70–80 MiB, but actual size depends on Electron and packaging.

For direct agent use, run from repository root with module mode:
python -m agents.router
Then paste a JSON request on stdin, such as {"agent":"shipping","payload":{"freight":100,"customs":20,"handling":5}}.

SQLite is a local, unencrypted placeholder stored at data/navaris_core.sqlite3 by default. Do not store confidential client data until local access controls, backups, and planned SQLCipher/AES protection are implemented and tested. No cloud database, Ollama, encryption proof, or outreach automation is included.
