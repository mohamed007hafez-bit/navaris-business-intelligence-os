"""Local-first opportunity scout. No live web discovery is implied."""
from __future__ import annotations

from typing import Iterable, Mapping, Any
import pandas as pd
import navaris_core as core

ILLUSTRATIVE_TENDERS = [
    {"name": "Borg Dekheila 20 trips", "value": 30000, "distance": 45, "selling": 1500,
     "source_status": "ILLUSTRATIVE — replace with verified RFQ"},
]


def scout_tenders(tenders: Iterable[Mapping[str, Any]] | None = None) -> pd.DataFrame:
    """Score supplied opportunity records; never label examples as live tenders."""
    results = []
    for tender in list(tenders if tenders is not None else ILLUSTRATIVE_TENDERS):
        name = str(tender.get("name", "")).strip()
        if not name:
            continue
        selling = float(tender.get("selling", 0) or 0)
        cost = core.calc_cost(
            float(tender.get("distance", 0) or 0),
            fuel_rate=float(tender.get("fuel_rate", 15) or 0),
            toll=float(tender.get("toll", 200) or 0),
            surcharge=float(tender.get("surcharge", 0) or 0),
        )
        profit = core.calc_profit(selling, cost)
        margin = profit / selling * 100 if selling else 0.0
        grade = core.evaluate_margin(margin)
        results.append({
            "Opportunity": name,
            "Value": float(tender.get("value", 0) or 0),
            "Cost": round(cost, 2),
            "Selling": round(selling, 2),
            "Profit": round(profit, 2),
            "Gross Margin %": round(margin, 2),
            "BCG": core.get_bcg_type(margin),
            "Grade": grade,
            "Evidence Status": tender.get("source_status", "UNVERIFIED — source required"),
            "Decision": "GO" if bool(tender.get("evidence_verified", False)) and margin >= 30 else ("HOLD" if margin < 20 else "VERIFY"),
        })
    return pd.DataFrame(results)
