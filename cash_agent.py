"""Illustrative monthly commission model with a fail-closed cash ledger.

The 30% split and sample trip data are scenario assumptions only. They are
not quotations, agreed entitlements, invoices, or evidence of collected cash.
"""
from __future__ import annotations

from typing import Iterable, Mapping, Any

import pandas as pd


ILLUSTRATIVE_COMMISSION_RATE = 0.30
ILLUSTRATIVE_MONTHLY_DATA = [
    {"Client": "Borg 20", "Trips": 20, "Price per trip": 1500},
    {"Client": "Alex 15", "Trips": 15, "Price per trip": 1800},
    {"Client": "Wardian 30", "Trips": 30, "Price per trip": 450},
    {"Client": "El Max 10", "Trips": 10, "Price per trip": 750},
    {"Client": "Low-bed 5", "Trips": 5, "Price per trip": 3000},
]


def calc_monthly_cash(
    data: Iterable[Mapping[str, Any]] | None = None,
) -> tuple[pd.DataFrame, dict[str, float]]:
    """Return scenario forecasts while keeping actual collected cash at zero.

    Any caller-supplied 'Actual Cash Collected' value is retained only as an
    unverified claim for review. This module has no bank-verification adapter
    and therefore cannot recognize any such value as collected cash.
    """
    rows = []
    for item in list(data if data is not None else ILLUSTRATIVE_MONTHLY_DATA):
        trips = float(item.get("Trips", 0) or 0)
        price = float(item.get("Price per trip", 0) or 0)
        if trips < 0 or price < 0:
            raise ValueError("Trips and price per trip must be non-negative")

        claimed_cash = float(item.get("Actual Cash Collected", 0) or 0)
        if claimed_cash < 0:
            raise ValueError("Unverified cash claim cannot be negative")

        invoices = trips * price
        scenario_share = invoices * ILLUSTRATIVE_COMMISSION_RATE
        supplied_status = str(item.get("Evidence Status", "NOT PROVIDED"))
        rows.append({
            "Client": item.get("Client", "Unnamed"),
            "Trips": trips,
            "Price per trip": price,
            "Scenario Transaction Value": invoices,
            "NAVARIS 30% Scenario Only": scenario_share,
            "Unverified Cash Claim": claimed_cash,
            "Actual Cash Collected": 0.0,
            "Evidence Status": (
                "PENDING_INDEPENDENT_BANK_VERIFICATION"
                if claimed_cash > 0
                else supplied_status
            ),
        })

    df = pd.DataFrame(rows)
    scenario_total = (
        float(df["NAVARIS 30% Scenario Only"].sum()) if not df.empty else 0.0
    )
    projection = {
        "5 clients (illustrative scenario)": scenario_total,
        "10 clients (simple 2x scenario)": scenario_total * 2,
        "20 clients (simple 4x scenario)": scenario_total * 4,
        "Actual cash collected (verified and approved)": 0.0,
    }
    return df, projection
