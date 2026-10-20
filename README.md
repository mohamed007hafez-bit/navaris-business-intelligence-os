# NAVARIS - Single Company - Alexandria - Dr. Mohamed Hafez Khalifa - One Main

**Company lock:** NAVARIS only; one company based in Alexandria, Egypt. No HAFEZ GROUP, holding company, or other companies.

## One Main architecture
- Dr. Mohamed Hafez Khalifa is the single master.
- `core/master.py` is the only task-assignment authority.
- 13 subordinate agents execute bounded tasks and report to the master; they cannot assign tasks to one another.
- Market: Egypt only in this version.
- Core: Business Doctor + Technical Services, informed by the owner's IOD rigless background (2012–2013).
- Storage: local SQLite. No paid APIs or API keys are needed.

## Install
Python 3.10+ recommended.
```bash
bash install.sh
```
The installer installs `fastapi` and `uvicorn`, then runs the master health check.

## Run local API
```bash
python mcp-server/server.py
```
Health endpoint: `http://127.0.0.1:8000/health`. The service binds to loopback by default.

## Master commands
```bash
python core/master.py health
python core/master.py --health
python core/master.py assign --agent 06 --task "Describe the task"
```
HTTP task assignment requires header `X-Navaris-Master-Key: NAVARIS-MASTER-2026` on local `POST /tasks`. Do not expose this key to public networks.

## Safety and limits
- Retry logic is bounded to 10 attempts.
- The orchestrator does not download or modify code automatically.
- This GitHub commit adds source files; it does not install dependencies or start a server on your device.
- Clients and subcontractors remain relationships of NAVARIS, not separate companies.
