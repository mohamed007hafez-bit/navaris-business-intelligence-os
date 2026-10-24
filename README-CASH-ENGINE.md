# NAVARIS AI CASH ENGINE v1.0
Nine separated verticals with specialist prompts and source boundaries.
- Source PDF convention: `agents/<vertical>/latest.pdf`
- Training script: `scripts/train_agents.py`
- Workflow: `.github/workflows/pdf-train.yml`
- Specialist definitions: `agents.json`
- WhatsApp sales prompt: `agents/whatsapp-sales-agent.md`
## Important setup
The source PDFs were not supplied in this request and are not fabricated. Upload the real PDF for each vertical.
The workflow requires a trusted Linux self-hosted GitHub Actions runner labeled `navaris-ollama` with Ollama installed and reachable locally. Configure repository variable `OLLAMA_HOST` (optional; defaults to localhost), `OLLAMA_EMBED_MODEL` (optional; defaults to `nomic-embed-text`), secret `OPENAI_API_KEY` for OpenAI embeddings, and optional variable `OPENAI_EMBED_MODEL`.
The requested counts total **19**, not 18: 3+2+2+3+1+2+2+2+2=19. All specified per-vertical counts are preserved in agents.json.
