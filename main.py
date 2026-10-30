"""NAVARIS OS — Local-first command-line entry point with Vault bootstrap."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import pandas as pd

from engines.legacy_route_pricing import build_excel_with_charts
from pricer_agent import price_route
from scout_agent import scout_tenders
from cash_agent import calc_monthly_cash
from ncnda_agent import generate_ncnda
from chatgpt_bridge import should_call_cloud
from src.core.secure_vault import SecureVault, VaultSecurityError

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
    # Fail closed: initialize encrypted local storage before processing any data.
    try:
        vault = SecureVault()
    except VaultSecurityError as exc:
        raise SystemExit(f"NAVARIS SECURITY STOP: {exc}") from exc

    parser = argparse.ArgumentParser(description="NAVARIS local-first pricing, opportunity and cash model.")
    parser.add_argument("--demo", action="store_true", help="Use illustrative example data from NAVARIS skill.")
    parser.add_argument("--input-json", type=Path, help="Optional JSON file containing routes, tenders and monthly_data.")
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT, help="Output XLSX path.")
    parser.add_argument("--approve-cloud", action="store_true",
                        help="Human approval for the cloud eligibility gate; no cloud request is sent by this app.")
    args = parser.parse_args()

    try:
        if args.input_json:
            payload = json.loads(args.input_json.read_text(encoding="utf-8"))
            route_data = payload.get("routes", [])
            tender_data = payload.get("tenders", [])
            monthly_data = payload.get("monthly_data", [])
        elif args.demo:
            route_data = [{"name": n, "distance": d, "toll": t, "surcharge": s, "selling": p} for n, d, t, s, p in ROUTES]
            tender_data = None
            monthly_data = None
            payload = {}
        else:
            parser.error("Provide --demo or --input-json. No live data is fetched automatically.")

        # Input financial material is encrypted into the Vault before analysis.
        if args.input_json:
            vault.put_financial_record("input_payload", payload)

        pricing_rows = [
            price_route(str(r["name"]), float(r["distance"]), float(r.get("toll", 200)),
                        float(r.get("surcharge", 0)), float(r["selling"]), float(r.get("fuel_rate", 15)))
            for r in route_data
        ]
        df_pricing = pd.DataFrame(pricing_rows)
        df_monthly, projection = calc_monthly_cash(monthly_data if monthly_data is not None and args.input_json else None)
        df_tenders = scout_tenders(tender_data)

        output = Path(args.output)
        output.parent.mkdir(parents=True, exist_ok=True)
        output_path = build_excel_with_charts(df_pricing, df_monthly, output)

        from openpyxl import load_workbook
        wb = load_workbook(output_path)
        ws = wb["Tenders_BCG"]
        if not df_tenders.empty:
            ws.append(list(df_tenders.columns))
            for row in df_tenders.itertuples(index=False, name=None):
                ws.append(list(row))
            ws.freeze_panes = "A2"
            ws.auto_filter.ref = ws.dimensions
        wb.save(output_path)

        draft_dir = output.parent / "drafts"
        drafts_created = 0
        for row in pricing_rows:
            client_name = str(payload.get("client_name", "")).strip()
            if client_name and row["Grade"] in ("ممتاز", "جيد جدا"):
                draft_dir.mkdir(parents=True, exist_ok=True)
                safe_name = "".join(ch if ch.isalnum() or ch in "-_" else "_" for ch in row["Route"])
                draft = generate_ncnda(client_name, row["Grade"])
                (draft_dir / f"NCNDA_DRAFT_{safe_name}.txt").write_text(draft, encoding="utf-8")
                drafts_created += 1

        best_grade = "ممتاز" if any(row["Grade"] == "ممتاز" for row in pricing_rows) else (
            "جيد جدا" if any(row["Grade"] == "جيد جدا" for row in pricing_rows) else "غير مقبول")
        cloud_gate = should_call_cloud(best_grade, manual_approval=args.approve_cloud)

        print("NAVARIS OS: SUCCESS")
        print(f"Workbook: {output_path}")
        print("Vault: SQLCipher + AES-256-GCM active")
        print(f"Vault audit chain valid: {vault.verify_audit_chain()}")
        print(f"Air-gapped mode configured: {SecureVault.is_offline()} (physical isolation must be enforced separately)")
        print("Evidence mode: DEMO / illustrative" if args.demo else "Evidence mode: supplied JSON; verify source records")
        print("Forecast is not cash collected. Actual cash collected remains evidence-based.")
        print("NAVARIS cash projection:", json.dumps(projection, ensure_ascii=False))
        print(f"NCNDA drafts created: {drafts_created} (non-binding; legal review required)")
        print(f"Cloud eligibility gate: {'PASSED — no request sent; provider integration is not configured' if cloud_gate else 'CLOSED — local-only'}")
        print("Decision: verify buyer, supplier, RFQ, costs, payment terms and written agreement before commitment.")
        return 0
    finally:
        vault.close()


if __name__ == "__main__":
    raise SystemExit(main())
