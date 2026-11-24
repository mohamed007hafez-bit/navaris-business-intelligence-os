"""NAVARIS OS entry point. GUI launches by default; CLI remains available."""
from __future__ import annotations

import argparse
import json
import sys
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
    try:
        vault = SecureVault()
    except VaultSecurityError as exc:
        raise SystemExit(f"NAVARIS SECURITY STOP: {exc}") from exc

    try:
        if len(sys.argv) == 1:
            from dashboard.app import run_app
            run_app(vault)
            return 0

        parser = argparse.ArgumentParser(description="NAVARIS local-first pricing, opportunity and cash model.")
        parser.add_argument("--demo", action="store_true")
        parser.add_argument("--input-json", type=Path)
        parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
        parser.add_argument("--approve-cloud", action="store_true")
        parser.add_argument("--company-name", default="")
        parser.add_argument("--consulting-sheet-type", choices=("consulting", "auditor", "training"))
        args = parser.parse_args()

        if args.consulting_sheet_type:
            from src.specializations.consulting.excel_factory import create_consulting_sheet
            type_map = {"consulting": "consulting_proposal", "auditor": "audit", "training": "training_plan"}
            import tempfile
            with tempfile.TemporaryDirectory(prefix="navaris-xlsx-") as temp_dir:
                workbook_path = create_consulting_sheet(
                    args.company_name or "Company", type_map[args.consulting_sheet_type], output_dir=temp_dir)
                vault_id = vault.encrypt_file(workbook_path, delete_source=True)
            print(f"Workbook encrypted and stored in SecureVault. Vault file ID: {vault_id}")
            print(f"Audit chain valid: {vault.verify_audit_chain()}")
            return 0

        if args.input_json:
            payload = json.loads(args.input_json.read_text(encoding="utf-8"))
            route_data = payload.get("routes", [])
            tender_data = payload.get("tenders", [])
            monthly_data = payload.get("monthly_data", [])
            vault.put_financial_record("input_payload", payload)
        elif args.demo:
            route_data = [{"name": n, "distance": d, "toll": t, "surcharge": s, "selling": p}
                          for n, d, t, s, p in ROUTES]
            tender_data, monthly_data, payload = None, None, {}
        else:
            parser.error("Provide --demo, --input-json, or --consulting-sheet-type.")

        pricing_rows = [
            price_route(str(r["name"]), float(r["distance"]), float(r.get("toll", 200)),
                        float(r.get("surcharge", 0)), float(r["selling"]), float(r.get("fuel_rate", 15)))
            for r in route_data]
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
        vault_file_id = vault.encrypt_file(output_path, file_id="navaris-operational-model", delete_source=True)
        print(f"Operational workbook encrypted in Vault. File ID: {vault_file_id}")

        drafts_created = 0
        for row in pricing_rows:
            client_name = str(payload.get("client_name", "")).strip()
            if client_name and row["Grade"] in ("ممتاز", "جيد جدا"):
                draft = generate_ncnda(client_name, row["Grade"])
                vault.put_financial_record(f"ncnda-draft-{drafts_created+1}", {"draft": draft})
                drafts_created += 1

        best_grade = "ممتاز" if any(row["Grade"] == "ممتاز" for row in pricing_rows) else (
            "جيد جدا" if any(row["Grade"] == "جيد جدا" for row in pricing_rows) else "غير مقبول")
        cloud_gate = should_call_cloud(best_grade, manual_approval=args.approve_cloud)
        print("NAVARIS OS: SUCCESS")
        print("Vault audit chain valid:", vault.verify_audit_chain())
        print("Forecast is not cash collected. Actual cash collected remains evidence-based.")
        print("NAVARIS cash projection:", json.dumps(projection, ensure_ascii=False))
        print(f"NCNDA drafts stored encrypted: {drafts_created}")
        print(f"Cloud eligibility gate: {'PASSED — no request sent' if cloud_gate else 'CLOSED — local-only'}")
        return 0
    finally:
        vault.close()


if __name__ == "__main__":
    raise SystemExit(main())
