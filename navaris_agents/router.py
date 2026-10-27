"""Central router: local deterministic dispatch only; no background execution or AI API calls."""
from __future__ import annotations

from typing import Any

from navaris_agents import config
from navaris_agents import financial, oilfield, shipping

AGENT_NAMES = {"shipping", "oilfield", "financial"}


def route_request(agent: str, action: str, payload: dict[str, Any], *,
                  enabled_agents: dict[str, bool] | None = None,
                  allow_cloud_ai: bool | None = None,
                  human_approved: bool = False) -> dict[str, Any]:
    """Dispatch a single explicit request to an enabled local handler."""
    agent = agent.strip().lower()
    action = action.strip().lower()
    enabled = config.ENABLED_AGENTS if enabled_agents is None else enabled_agents
    cloud_allowed = config.ALLOW_CLOUD_AI if allow_cloud_ai is None else allow_cloud_ai
    if agent not in AGENT_NAMES:
        raise ValueError(f"Unknown agent: {agent}")
    if not enabled.get(agent, False):
        raise PermissionError(f"Agent '{agent}' is disabled in NAVARIS settings")
    if cloud_allowed:
        if not human_approved:
            raise PermissionError("Cloud AI requires explicit human approval")
        raise NotImplementedError("No cloud AI provider is configured; no external request was sent")
    if agent == "shipping" and action == "landed_cost":
        result = shipping.calculate_landed_cost(shipping.ShippingCost(**payload))
    elif agent == "shipping" and action == "documents":
        result = shipping.documentation_checklist(**payload)
    elif agent == "oilfield" and action == "tender_review":
        result = oilfield.assess_tender(**payload)
    elif agent == "oilfield" and action == "risk_register":
        result = oilfield.project_risk_register(payload.get("items", []))
    elif agent == "financial" and action == "cashflow":
        result = financial.summarize_cashflow(payload.get("rows", []))
    elif agent == "financial" and action == "profitability":
        result = financial.profitability(**payload)
    else:
        raise ValueError(f"Unsupported action '{action}' for agent '{agent}'")
    return {"agent": agent, "action": action, "execution_mode": "LOCAL_ONLY",
            "external_calls": 0, "result": result}
