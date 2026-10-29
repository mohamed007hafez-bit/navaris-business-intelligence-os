"""NAVARIS OS fixed core.

Core policy: keep formulas and thresholds stable; make changes through tests and
versioned change requests. All default examples are illustrative, not live deals.
"""
from __future__ import annotations

from pathlib import Path
from typing import Any

import pandas as pd
from openpyxl import load_workbook
from openpyxl.chart import BarChart, PieChart, Reference
from openpyxl.styles import PatternFill


def calc_cost(distance: float, fuel_rate: float = 15, toll: float = 200, surcharge: float = 0) -> float:
    """Cost = Distance × Fuel/route rate + Toll + Surcharge."""
    values = (distance, fuel_rate, toll, surcharge)
    if any(float(value) < 0 for value in values):
        raise ValueError("Distance, rates, toll and surcharge must be non-negative.")
    return float(distance) * float(fuel_rate) + float(toll) + float(surcharge)


def calc_profit(selling: float, cost: float) -> float:
    """Gross deal profit = selling price − total cost."""
    if float(selling) < 0 or float(cost) < 0:
        raise ValueError("Selling price and cost must be non-negative.")
    return float(selling) - float(cost)


def calc_share_30_70(selling: float, cost: float) -> tuple[float, float, float]:
    """Illustrative commercial split: 30% NAVARIS / 70% operating company.

    The 30/70 basis is sales revenue, as written in the supplied NAVARIS skill.
    It is not a default legal entitlement; use only when the parties agree in writing.
    """
    if float(selling) < 0 or float(cost) < 0:
        raise ValueError("Selling price and cost must be non-negative.")
    navaris_share = float(selling) * 0.30
    company_share = float(selling) * 0.70
    company_net = company_share - float(cost)
    return navaris_share, company_share, company_net


def calc_ratios(cost: float, selling: float, profit: float, company_net: float, company_70: float) -> dict[str, float]:
    """Return ratios as percentages; zero denominator returns 0."""
    gross_margin = (profit / selling * 100) if selling else 0.0
    operating_ratio = (cost / selling * 100) if selling else 0.0
    company_margin = (company_net / company_70 * 100) if company_70 else 0.0
    return {
        "Gross Margin %": gross_margin,
        "Operating Ratio %": operating_ratio,
        "Company Net %": company_margin,
    }


def evaluate_margin(margin: float) -> str:
    if margin < 20:
        return "غير مقبول"
    if margin < 30:
        return "مقبول"
    if margin < 40:
        return "جيد"
    if margin < 50:
        return "جيد جدا"
    return "ممتاز"


def get_bcg_type(margin: float) -> str:
    """NAVARIS's simplified margin bands; not the original market-share BCG matrix."""
    if margin > 50:
        return "STAR – ممتاز – اشتغل فورا"
    if margin >= 40:
        return "CASH COW – جيد جدا – استمر"
    if margin >= 20:
        return "QUESTION – مقبول – راجع"
    return "DOG – غير مقبول – لا تشتغل"


def get_color_fill(grade: str) -> PatternFill:
    fills = {
        "ممتاز": "00FF00",
        "جيد جدا": "90EE90",
        "جيد": "FFFF00",
        "مقبول": "FFA500",
        "غير مقبول": "FF0000",
    }
    colour = fills.get(grade)
    return PatternFill(start_color=colour, end_color=colour, fill_type="solid") if colour else PatternFill()


def build_excel_with_charts(df_pricing: pd.DataFrame, df_monthly: pd.DataFrame, output_path: str | Path) -> str:
    """Build an actual Excel workbook with editable data, grading and native charts."""
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    tender_columns = ["المناقصة", "القيمة", "هامش %", "BCG", "التقييم"]
    with pd.ExcelWriter(path, engine="openpyxl") as writer:
        df_pricing.to_excel(writer, sheet_name="Pricing_Grading", index=False)
        df_monthly.to_excel(writer, sheet_name="Monthly_30pct", index=False)
        pd.DataFrame(columns=tender_columns).to_excel(writer, sheet_name="Tenders_BCG", index=False)

    wb = load_workbook(path)
    ws = wb["Pricing_Grading"]
    for cell in ws[1]:
        cell.font = cell.font.copy(bold=True)
    ws.freeze_panes = "A2"
    ws.auto_filter.ref = ws.dimensions
    headers = {str(cell.value): cell.column for cell in ws[1] if cell.value is not None}

    def add_bar(title: str, y_title: str, column_names: list[str], anchor: str) -> None:
        available = [headers[name] for name in column_names if name in headers]
        if not available or ws.max_row < 2:
            return
        chart = BarChart()
        chart.title = title
        chart.y_axis.title = y_title
        data = Reference(ws, min_col=min(available), max_col=max(available), min_row=1, max_row=ws.max_row)
        chart.add_data(data, titles_from_data=True)
        route_col = headers.get("Route") or headers.get("المسار")
        if route_col:
            chart.set_categories(Reference(ws, min_col=route_col, min_row=2, max_row=ws.max_row))
        ws.add_chart(chart, anchor)

    add_bar("Profit Split 30/70", "Currency", ["Your 30%", "Company 70%"], "L2")
    add_bar("Gross Margin %", "Percent", ["Gross Margin %"], "L18")

    grade_col = headers.get("Grade") or headers.get("التقييم")
    if grade_col:
        for row in range(2, ws.max_row + 1):
            ws.cell(row=row, column=grade_col).fill = get_color_fill(str(ws.cell(row=row, column=grade_col).value or ""))

    ws2 = wb["Monthly_30pct"]
    if ws2.max_row >= 2 and ws2.max_column >= 1:
        amount_col = headers2 = {str(cell.value): cell.column for cell in ws2[1] if cell.value is not None}
        share_col = next((v for k, v in headers2.items() if "30%" in k or "NAVARIS" in k), ws2.max_column)
        pie = PieChart()
        pie.title = "Illustrative Monthly NAVARIS Share"
        pie.add_data(Reference(ws2, min_col=share_col, min_row=1, max_row=ws2.max_row), titles_from_data=True)
        pie.set_categories(Reference(ws2, min_col=1, min_row=2, max_row=ws2.max_row))
        ws2.add_chart(pie, "G2")
    for sheet in wb.worksheets:
        for cell in sheet[1]:
            cell.font = cell.font.copy(bold=True)
        sheet.freeze_panes = "A2"
        sheet.auto_filter.ref = sheet.dimensions if sheet.max_row and sheet.max_column else None
    wb.save(path)
    return str(path)
