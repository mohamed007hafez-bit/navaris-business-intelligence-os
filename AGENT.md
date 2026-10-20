# NAVARIS - SINGLE COMPANY - ALEXANDRIA v4.1 FINAL LOCKED

ROLE: You are building OS for NAVARIS - One Company Only.
OWNER: Dr. Mohamed Hafez Khalifa - Alexandria, Egypt - ONE MAIN MASTER ONLY
COMPANY: NAVARIS - Single entity - Locked - Do not create HAFEZ GROUP, holding, or other companies

BUSINESS LOCKED:
- Base: Alexandria, Egypt
- Market: Egypt only (no GCC in this version)
- Core: Business Doctor + Technical Services (Rigless background IOD 2012-13)
- Clients: Nasr Civil Works, Al Fanar Contracting, Cresting Mark = CLIENTS of NAVARIS, not companies
- Partner: Maridive & Oil Services = subcontractor ONLY
- Diagnostic Fee: $25-50k - 250k EGP is too low for Enppi
- Start: Egypt

ARCHITECTURE - ONE MAIN:
- Master = Dr. Mohamed - core/master.py - ONLY file that can give orders - Has MASTER_KEY = "NAVARIS-MASTER-2026"
- Slaves = 13 agents - core/slave.py - They can only report_to_master() and execute_task() - CANNOT control master
- All commands go through master: python core/master.py assign --agent 06 --task "..."
- Rule: Slaves cannot talk to each other directly, only to master

STACK: Zero cost - Python + FastAPI + SQLite - No paid APIs - No keys - Auto-fix 10 retries - Never ask user for money

BUILD NOW - FILES REQUIRED:
1. /core/master.py
2. /core/slave.py
3. /core/orchestrator.py (health + upgrade)
4. /mcp-server/server.py (FastAPI local port 8000)
5. /agents/ 13 files - Each file header: "# Works for NAVARIS only - Single Company"
6. /install.sh - One-click: bash install.sh -> installs and runs
7. README.md - Title: NAVARIS - Alexandria - Single Company - One Main
8. requirements.txt - fastapi, uvicorn only

COMMIT MESSAGE: "feat: NAVARIS single company Alexandria v4.1 - name locked - one main"

HARD RULE: DO NOT CREATE OTHER COMPANIES. ONE COMPANY = NAVARIS ONLY. DO NOT FABRICATE.
