"""Opt-in FastAPI wrapper around the local NAVARIS router."""
from __future__ import annotations

from typing import Any

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from navaris_agents import config
from navaris_agents.router import route_request

app = FastAPI(title="NAVARIS Business Toolkits API", version="1.0.0")


class RouteRequest(BaseModel):
    agent: str
    action: str
    payload: dict[str, Any] = Field(default_factory=dict)
    human_approved: bool = False


@app.get("/health")
def health() -> dict[str, Any]:
    return {"status": "ok", "mode": "local-first", "cloud_ai_enabled": config.ALLOW_CLOUD_AI,
            "enabled_agents": config.ENABLED_AGENTS}


@app.post("/route")
def route(body: RouteRequest) -> dict[str, Any]:
    try:
        return route_request(body.agent, body.action, body.payload, human_approved=body.human_approved)
    except PermissionError as exc:
        raise HTTPException(status_code=403, detail=str(exc)) from exc
    except NotImplementedError as exc:
        raise HTTPException(status_code=501, detail=str(exc)) from exc
    except (TypeError, ValueError) as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
