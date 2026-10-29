"""Pricing agent built on the immutable NAVARIS core formulas."""
from __future__ import annotations
from typing import Any
import engines.legacy_route_pricing as core


def price_route(route_name: str, distance: float, toll: float, surcharge: float, selling: float,
                fuel_rate: float = 15) -> dict[str, Any]:
    cost = core.calc_cost(distance, fuel_rate=fuel_rate, toll=toll, surcharge=surcharge)
    profit = core.calc_profit(selling, cost)
    navaris_30, company_70, company_net = core.calc_share_30_70(selling, cost)
    ratios = core.calc_ratios(cost, selling, profit, company_net, company_70)
    grade = core.evaluate_margin(ratios["Gross Margin %"])
    return {
        "Route": route_name, "Distance": distance, "Cost": round(cost, 2),
        "Selling": round(selling, 2), "Profit": round(profit, 2),
        "Your 30%": round(navaris_30, 2), "Company 70%": round(company_70, 2),
        "Company Net": round(company_net, 2),
        "Gross Margin %": round(ratios["Gross Margin %"], 2),
        "Operating Ratio %": round(ratios["Operating Ratio %"], 2),
        "Company Net %": round(ratios["Company Net %"], 2),
        "Grade": grade, "BCG": core.get_bcg_type(ratios["Gross Margin %"]),
        "Decision": "HOLD — company net negative" if company_net < 0 else ("VERIFY — written agreement required" if grade in ("ممتاز", "جيد جدا") else "REVIEW — do not commit yet"),
        "Evidence Status": "ILLUSTRATIVE INPUT — verify price, cost and route before use",
    }
