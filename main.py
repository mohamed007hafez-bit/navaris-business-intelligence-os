"""NAVARIS OS — Local Hybrid entry point.

Run locally with: python main.py --demo
The demo uses illustrative values from the supplied NAVARIS skill and is not live market data.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import pandas as pd

from navaris_core import build_excel_with_charts
from pricer_agent import price_route
from scout_agent import scout_tenders
from cash_agent import calc_monthly_cash

BASE_DIR = Path(__file__).resolve().parent
DEFAULT_OUTPUT = BASE_DIR / "output" / "NAVARIS_Agnatics_OS_FINAL.xlsx"
ROUTES = [
    ("Borg -> Dekheila", 45, 200, 0, 1500),
    ("Borg -> Alex", 55, 250, 0, 1800),
    ("El Max -> Dekheila", 15, 100, 100, 750),
    ("Wardian -> Dekheila", 10, 80, 0, 450),
    ("Low-bed Alstom", 5, 0, 500, 3000),
]


def main() -> int:
    parser = argparse.ArgumentParser(description="NAVARIS local-first pricing, opportunity and cash model.")
    parser.add_argument("--demo", action="store_true", help="Use illustrative example data from NAVARIS skill.")
    parser.add_argument("--input-json", type=Path, help="Optional JSON file containing routes, tenders and monthly_data.")
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT, help="Output XLSX path.")
    args = parser.parse_args()

    if args.input_json:
        payload = json.loads(args.input_json.read_text(encoding="utf-8"))
        route_data = payload.get("routes", [])
        tender_data = payload.get("tenders", [])
        monthly_data = payload.get("monthly_data", [])
    elif args.demo:
        route_data = [{"name": n, "distance": d, "toll": t, "surcharge": s, "selling": p} for n, d, t, s, p in ROUTES]
        tender_data = None
        monthly_data = None
    else:
        parser.error("Provide --demo or --input-json. No live data is fetched automatically.")

    pricing_rows = [
        price_route(
            str(r["name"]), float(r["distance"]), float(r.get("toll", 200)),
            float(r.get("surcharge", 0)), float(r["selling"]), float(r.get("fuel_rate", 15))
        )
        for r in route_data
    ]
    df_pricing = pd.DataFrame(pricing_rows)
    df_monthly, projection = calc_monthly_cash(monthly_data if monthly_data else None)
    df_tenders = scout_tenders(tender_data)
    output = build_excel_with_charts(df_pricing, df_monthly, args.output)

    # Add tender data to its native Excel sheet without flattening it into an image.
    from openpyxl import load_workbook
    wb = load_workbook(output)
    ws = wb["Tenders_BCG"]
    if not df_tenders.empty:
        ws.append(list(df_tenders.columns))
        for row in df_tenders.itertuples(index=False, name=None):
            ws.append(list(row))
        ws.freeze_panes = "A2"
        ws.auto_filter.ref = ws.dimensions
    wb.save(output)

    print("NAVARIS OS: SUCCESS")
    print(f"Workbook: {output}")
    print("Evidence mode: DEMO / illustrative" if args.demo else "Evidence mode: supplied JSON; verify source records")
    print("Forecast is not cash collected. Actual cash collected remains evidence-based.")
    print("NAVARIS cash projection:", json.dumps(projection, ensure_ascii=False))
    print("Decision: verify actual buyer, supplier, RFQ, costs, payment terms and written agreement before commitment.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
