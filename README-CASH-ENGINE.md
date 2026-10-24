# NAVARIS AI CASH ENGINE v1.0
Nine separated verticals with specialist prompts and source boundaries.
- Source PDF convention: `agents/<vertical>/latest.pdf`
- Training script: `scripts/train_agents.py`
- Workflow: `.github/workflows/pdf-train.yml`
- Specialist definitions: `agents.json`
- WhatsApp sales prompt: `agents/whatsapp-sales-agent.md`

## Setup
Source PDFs were not supplied in this request and are not fabricated. Upload the real PDF for each vertical.
The workflow requires a trusted Linux self-hosted GitHub Actions runner labeled `navaris-ollama` with Ollama installed and reachable locally. Configure `OLLAMA_HOST` (optional; defaults to localhost), `OLLAMA_EMBED_MODEL` (optional; defaults to `nomic-embed-text`), secret `OPENAI_API_KEY`, and optional `OPENAI_EMBED_MODEL`.

**Count discrepancy:** the requested vertical counts total 19, not 18: 3+2+2+3+1+2+2+2+2=19. Per-vertical counts will be preserved.