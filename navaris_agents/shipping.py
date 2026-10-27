"""International shipping cost and documentation toolkit; estimates are not live quotes."""
from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any


@dataclass(frozen=True)
class ShippingCost:
    goods_value: float
    freight: float
    insurance: float = 0.0
    origin_charges: float = 0.0
    destination_charges: float = 0.0
    duties_and_taxes: float = 0.0
    other_costs: float = 0.0

    def validate(self) -> None:
        for key, value in asdict(self).items():
            if not isinstance(value, (int, float)) or value < 0:
                raise ValueError(f"{key} must be a non-negative number")


def calculate_landed_cost(cost: ShippingCost, margin_pct: float = 0.0) -> dict[str, Any]:
    """Calculate an indicative landed cost from user-supplied, evidenced inputs."""
    cost.validate()
    if not 0 <= margin_pct <= 1000:
        raise ValueError("margin_pct must be between 0 and 1000")
    total = sum(asdict(cost).values())
    return {
        "status": "ESTIMATE_ONLY",
        "currency": "USER_SPECIFIED",
        "cost_breakdown": asdict(cost),
        "landed_cost": round(total, 2),
        "margin_pct": margin_pct,
        "indicative_sell_price": round(total * (1 + margin_pct / 100), 2),
        "evidence_required": [
            "Written carrier/forwarder quote and validity date",
            "Incoterms rule and named place",
            "HS classification and official duty/tax confirmation",
            "Insurance terms and destination/origin charges",
        ],
        "warning": "Not a carrier quote, customs ruling, tax opinion, or verified market price.",
    }


def documentation_checklist(mode: str = "sea") -> dict[str, Any]:
    """Return a generic checklist; requirements must be verified for the shipment."""
    mode = mode.strip().lower()
    if mode not in {"sea", "air", "road"}:
        raise ValueError("mode must be sea, air, or road")
    common = ["Commercial invoice", "Packing list", "HS code/classification review",
              "Importer/exporter details", "Incoterms and named place", "Insurance decision"]
    transport = {
        "sea": ["Bill of lading instructions", "Booking confirmation", "Verified port charges"],
        "air": ["Air waybill instructions", "Airline booking", "Verified handling charges"],
        "road": ["CMR/road consignment note as applicable", "Border/transit documents", "Verified route permits"],
    }
    return {"mode": mode, "status": "CHECKLIST_ONLY", "items": common + transport[mode],
            "note": "Confirm country-, commodity-, and transaction-specific requirements with the broker/carrier."}
