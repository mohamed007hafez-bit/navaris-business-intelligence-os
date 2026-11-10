"""NAVARIS local API. All workflows are user-triggered, draft-only, and local."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from fastapi import FastAPI
from pydantic import BaseModel, Field

from backend.workflow import AGENT_SEQUENCE, run_workflow

app = FastAPI(title="NAVARIS Local Business Operations API", version="2.1.0")


class WorkflowRequest(BaseModel):
    sector: str = ""
    problem: str = ""
    facts: list[dict[str, Any]] = Field(default_factory=list)
    risks: list[dict[str, Any]] = Field(default_factory=list)
    notes: str = ""


@app.get("/health")
def health() -> dict[str, str]:
    return {
        "status": "ok",
        "service": "NAVARIS Local API",
        "version": "2.1.0",
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


@app.get("/agents/status")
def agents_status() -> dict[str, Any]:
    return {
        "status": "READY_FOR_LOCAL_TESTING",
        "mode": "deterministic, local, user-triggered",
        "agents": list(AGENT_SEQUENCE),
        "autonomous_background_execution": False,
        "external_actions": False,
        "ai_provider_configured": False,
        "human_review_required": True,
    }


@app.post("/workflow/run")
def workflow_run(request: WorkflowRequest) -> dict[str, Any]:
    """Run local deterministic agents; this endpoint never sends or stores data."""
    return run_workflow(request.model_dump())


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("backend.main:app", host="127.0.0.1", port=8000, reload=False)
