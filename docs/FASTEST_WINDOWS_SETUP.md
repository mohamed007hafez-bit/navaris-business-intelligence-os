# Fastest safe NAVARIS local setup on Windows

The development branch contains the client-facing preview and the deterministic, user-triggered local workflow API. Use a separate working folder; do not overwrite or delete your existing NAVARIS project folders.

## Install only the required tools

1. Git for Windows (to clone/update this GitHub project).
2. Node.js 20 LTS (includes npm; required by the Next.js client portal).
3. Python 3.12 (or 3.11; required by the FastAPI local API).
4. VS Code is optional. Git and Node/Python installers should be obtained from their official vendor websites, not from random GitHub release assets. The application source code comes from this repository.

If Python 3.15 is already installed, keep it; install Python 3.12 alongside it for this project's dependencies. Do not place API keys or client records in the source repository.

## Get the current development branch

Open Command Prompt in the folder where you want the project, then run:

```bat
git clone https://github.com/mohamed007hafez-bit/navaris-business-intelligence-os.git
cd navaris-business-intelligence-os
git checkout docs/navaris-launch-roadmap
```

Alternatively, download the source archive for the development branch:

`https://github.com/mohamed007hafez-bit/navaris-business-intelligence-os/archive/refs/heads/docs/navaris-launch-roadmap.zip`

Git is recommended because it makes updating the project easier.

## Start both local components

Double-click `start_navaris_local.bat`. On first run it creates a local Python virtual environment, installs the repository's Python dependencies, installs the app's npm packages, starts both development servers, and opens the client preview.

- Client preview: `http://localhost:3000`
- Local API documentation: `http://127.0.0.1:8000/docs`
- Agent status: `http://127.0.0.1:8000/agents/status`

The script requires Node.js and Python to be installed first; it does not download or silently install system software. Keep both command windows open while using NAVARIS. Close them to stop the local servers.

## Test the current workflow agents

From the repository root, run:

```bat
.venv\Scripts\python.exe -m unittest tests.test_local_workflow -v
```

The current agents are deterministic local workflow steps, not an unattended autonomous service. They do not research the internet, make decisions on behalf of the founder, save data to a server, or contact clients. The enquiry form saves to the current browser only. Do not enter sensitive or real customer/bank information in this preview.

## Limit of this setup

This launches a development preview on your computer, not a production client platform. Multi-user accounts, secure database persistence, document upload, backups, audit trail, production deployment, and security acceptance testing are still required before collecting real customer data or launching publicly. The coding agent can change the GitHub branch, but cannot install these tools on your PC or verify your local device without you running the setup and sharing non-secret error messages.
