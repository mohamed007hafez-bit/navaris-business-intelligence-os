"""Monthly commission model. Forecasts are not cash collected."""
from __future__ import annotations
from typing import Iterable, Mapping, Any
import pandas as pd

ILLUSTRATIVE_MONTHLY_DATA = [
    {"Client": "Borg 20", "Trips": 20, "Price per trip": 1500},
    {"Client": "Alex 15", "Trips": 15, "Price per trip": 1800},
    {"Client": "Wardian 30", "Trips": 30, "Price per trip": 450},
    {"Client": "El Max 10", "Trips": 10, "Price per trip": 750},
    {"Client": "Low-bed 5", "Trips": 5, "Price per trip": 3000},
]


def calc_monthly_cash(data: Iterable[Mapping[str, Any]] | None = None) -> tuple[pd.DataFrame, dict[str, float]]:
    rows = []
    for item in list(data if data is not None else ILLUSTRATIVE_MONTHLY_DATA):
        trips = float(item.get("Trips", 0) or 0)
        price = float(item.get("Price per trip", 0) or 0)
        invoices = trips * price
        navaris_share = invoices * 0.30
        rows.append({
            "Client": item.get("Client", "Unnamed"),
            "Trips": trips,
            "Price per trip": price,
            "Invoices": invoices,
            "NAVARIS 30% (illustrative)": navaris_share,
            "Actual Cash Collected": float(item.get("Actual Cash Collected", 0) or 0),
            "Evidence Status": item.get("Evidence Status", "ILLUSTRATIVE — not a real customer"),
        })
    df = pd.DataFrame(rows)
    total = float(df["NAVARIS 30% (illustrative)"].sum()) if not df.empty else 0.0
    collected = float(df["Actual Cash Collected"].sum()) if not df.empty else 0.0
    projection = {
        "5 clients (illustrative base)": total,
        "10 clients (simple 2x scenario)": total * 2,
        "20 clients (simple 4x scenario)": total * 4,
        "Actual cash collected (evidence-based)": collected,
    }
    return df, projection
