"""Private, offline Excel workbook factory for NAVARIS consulting services.

Requires openpyxl. All workbook generation is local; this module performs no
network requests and does not transmit company data.
"""
from __future__ import annotations

import re
from datetime import date
from pathlib import Path
from typing import Callable

from openpyxl import Workbook
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.worksheet import Worksheet

ROOT_EMAIL = "mohamed007hafez@gmail.com"
ROOT_SIGNATURE = f"NAVARIS ROOT | {ROOT_EMAIL}"
BRAND = "NAVARIS OS - Private AI"
SUPPORTED_TYPES = {"audit", "training_plan", "consulting_proposal"}

NAVY = "0A1F44"
GOLD = "D4AF37"
IVORY = "FFFBF0"
WHITE = "FFFFFF"
PALE_BLUE = "EAF0F7"
PALE_GOLD = "F7F0D8"
GREY = "667085"
THIN_GOLD = Side(style="thin", color=GOLD)


def _safe_filename(company_name: str) -> str:
    cleaned = re.sub(r"[^A-Za-z0-9._-]+", "_", company_name.strip()).strip("._")
    return (cleaned or "Company")[:80]


def _add_header(ws: Worksheet, company_name: str, title: str) -> None:
    """Add the required private-company identity block to every worksheet."""
    ws.sheet_view.showGridLines = False
    ws.merge_cells("A1:F1")
    ws["A1"] = BRAND
    ws["A1"].font = Font(name="Aptos Display", size=16, bold=True, color=WHITE)
    ws["A1"].fill = PatternFill("solid", fgColor=NAVY)
    ws["A1"].alignment = Alignment(vertical="center")
    ws.row_dimensions[1].height = 30

    metadata = (
        ("A2", "Company Name", "B2", company_name),
        ("D2", "Date", "E2", date.today()),
        ("A3", "ROOT Signature", "B3", ROOT_SIGNATURE),
    )
    for label_cell, label, value_cell, value in metadata:
        ws[label_cell] = label
        ws[label_cell].font = Font(bold=True, color=NAVY)
        ws[value_cell] = value
        ws[value_cell].font = Font(color=GREY)
    ws["E2"].number_format = "dd-mmm-yyyy"
    ws.merge_cells("B3:F3")
    ws["B3"].font = Font(italic=True, color=NAVY)
    ws["A4"] = title
    ws["A4"].font = Font(size=13, bold=True, color=NAVY)
    ws["A4"].fill = PatternFill("solid", fgColor=PALE_GOLD)
    ws.merge_cells("A4:F4")
    ws.row_dimensions[4].height = 23


def _add_table(ws: Worksheet, headers: list[str], rows: list[list[object]]) -> None:
    header_row = 6
    for col, value in enumerate(headers, start=1):
        cell = ws.cell(header_row, col, value)
        cell.font = Font(bold=True, color=WHITE)
        cell.fill = PatternFill("solid", fgColor=NAVY)
        cell.alignment = Alignment(wrap_text=True, vertical="center")
        cell.border = Border(bottom=THIN_GOLD)
    ws.row_dimensions[header_row].height = 30

    for row_index, row in enumerate(rows, start=header_row + 1):
        for col_index, value in enumerate(row, start=1):
            cell = ws.cell(row_index, col_index, value)
            cell.alignment = Alignment(vertical="top", wrap_text=True)
            if row_index % 2:
                cell.fill = PatternFill("solid", fgColor=PALE_BLUE)
        ws.row_dimensions[row_index].height = 32

    ws.freeze_panes = "A7"
    ws.auto_filter.ref = f"A{header_row}:{get_column_letter(len(headers))}{header_row + len(rows)}"
    for col_index, header in enumerate(headers, start=1):
        values = [len(str(header))]
        values.extend(len(str(ws.cell(r, col_index).value or "")) for r in range(7, 7 + len(rows)))
        ws.column_dimensions[get_column_letter(col_index)].width = min(max(max(values) + 3, 15), 42)


def _audit_workbook(wb: Workbook, company_name: str) -> None:
    ws = wb.active
    ws.title = "Audit Checklist"
    _add_header(ws, company_name, "Management System Audit Checklist")
    rows = [
        ["Governance", "Defined responsibilities and delegated authority", "", "Open", 3, 3],
        ["Process", "Documented process controls and current procedures", "", "Open", 3, 4],
        ["Finance", "Revenue, cost and cash reconciliations are evidenced", "", "Open", 4, 5],
        ["People", "Competence and training records are maintained", "", "Open", 2, 3],
        ["Risk", "Operational risks have owners and mitigation actions", "", "Open", 3, 4],
        ["Compliance", "Applicable legal and contractual obligations are tracked", "", "Open", 4, 5],
    ]
    _add_table(ws, ["Area", "Audit question", "Evidence / reference", "Status", "Likelihood (1-5)", "Impact (1-5)"], rows)
    ws["G6"] = "Risk Score"
    ws["G6"].font = Font(bold=True, color=WHITE)
    ws["G6"].fill = PatternFill("solid", fgColor=NAVY)
    ws.column_dimensions["G"].width = 15
    for row in range(7, 7 + len(rows)):
        ws.cell(row, 7, f"=E{row}*F{row}")
        ws.cell(row, 7).number_format = "0"
    ws["A15"] = "Scoring guide: 1 = low; 5 = very high. Risk Score = Likelihood × Impact."
    ws.merge_cells("A15:G15")
    ws["A15"].font = Font(italic=True, color=GREY)

    risk = wb.create_sheet("Findings Register")
    _add_header(risk, company_name, "Audit Findings and Corrective Action Register")
    _add_table(
        risk,
        ["Finding ID", "Requirement / criterion", "Evidence", "Finding / gap", "Risk (1-25)", "Owner", "Due date", "Closure evidence"],
        [["AUD-001", "", "", "", "", "", "", ""]],
    )


def _training_workbook(wb: Workbook, company_name: str) -> None:
    ws = wb.active
    ws.title = "Training Roadmap"
    _add_header(ws, company_name, "Training Needs Analysis and Delivery Plan")
    _add_table(
        ws,
        ["Module", "Target audience", "Learning outcome", "Method", "Duration (hrs)", "Trainer", "Target date", "Assessment / evidence"],
        [
            ["Business process fundamentals", "Department leads", "Map and control core workflows", "Workshop", 4, "", "", ""],
            ["KPI and financial literacy", "Managers", "Interpret operational and cash KPIs", "Workshop", 4, "", "", ""],
            ["Risk-based problem solving", "Process owners", "Prioritize risks and corrective actions", "Case study", 3, "", "", ""],
        ],
    )
    matrix = wb.create_sheet("Competency Matrix")
    _add_header(matrix, company_name, "Role-Based Competency and Assessment Matrix")
    _add_table(
        matrix,
        ["Role", "Required competency", "Current level (1-5)", "Target level (1-5)", "Gap", "Development action", "Verification"],
        [
            ["Manager", "KPI interpretation", "", 4, "=IF(OR(C7=\"\",D7=\"\"),\"\",D7-C7)", "", ""],
            ["Process owner", "Risk assessment", "", 4, "=IF(OR(C8=\"\",D8=\"\"),\"\",D8-C8)", "", ""],
        ],
    )


def _consulting_workbook(wb: Workbook, company_name: str) -> None:
    ws = wb.active
    ws.title = "SWOT Analysis"
    _add_header(ws, company_name, "Strategic SWOT Assessment")
    _add_table(
        ws,
        ["Strengths", "Weaknesses", "Opportunities", "Threats", "Evidence / source", "Strategic implication"],
        [["", "", "", "", "", ""]],
    )

    plan = wb.create_sheet("Action Plan")
    _add_header(plan, company_name, "Prioritized Consulting Action Plan")
    _add_table(
        plan,
        ["Priority", "Workstream", "Action / deliverable", "Owner", "Start date", "Due date", "KPI / target", "Status"],
        [
            ["P0", "Cash", "Validate receivables and build a collection plan", "", "", "", "Cash collected", "Proposed"],
            ["P1", "Operations", "Map bottlenecks and quantify cost / time losses", "", "", "", "Cycle time / unit cost", "Proposed"],
            ["P2", "Governance", "Assign control owners and review cadence", "", "", "", "Actions closed on time", "Proposed"],
        ],
    )

    cash = wb.create_sheet("Cash Flow Impact")
    _add_header(cash, company_name, "Illustrative Cash Flow Impact Model")
    _add_table(
        cash,
        ["Initiative", "One-time cost", "Monthly savings", "Monthly cash uplift", "Implementation month", "12-month net impact", "Assumption / evidence"],
        [
            ["Working capital improvement", 0, 0, 0, 1, "=D7*12-B7", "Replace zero placeholders with validated inputs."],
            ["Procurement / logistics optimization", 0, 0, 0, 1, "=D8*12-B8", "Savings require baseline and supplier evidence."],
            ["Process productivity", 0, 0, 0, 1, "=D9*12-B9", "Do not treat forecast as collected cash."],
        ],
    )
    for row in range(7, 10):
        for col in (2, 3, 4, 6):
            cash.cell(row, col).number_format = '#,##0.00;[Red](#,##0.00);-'
    cash["A12"] = "All figures are illustrative placeholders until supported by client-approved evidence."
    cash.merge_cells("A12:G12")
    cash["A12"].font = Font(italic=True, color=GREY)


_BUILDERS: dict[str, Callable[[Workbook, str], None]] = {
    "audit": _audit_workbook,
    "training_plan": _training_workbook,
    "consulting_proposal": _consulting_workbook,
}


def create_consulting_sheet(
    company_name: str,
    type: str,
    output_dir: str | Path | None = None,
) -> Path:
    """Create a private Excel workbook locally and return its absolute path.

    Args:
        company_name: Company or client name shown in every worksheet.
        type: One of 'audit', 'training_plan', or 'consulting_proposal'.
        output_dir: Optional local destination. Defaults to the user's
            Documents/NavarisOS/Generated directory.

    No network access is performed. Existing files with the same name are
    replaced so repeat runs remain deterministic.
    """
    if not isinstance(company_name, str) or not company_name.strip():
        raise ValueError("company_name must be a non-empty string.")
    if not isinstance(type, str) or type not in SUPPORTED_TYPES:
        raise ValueError(f"type must be one of: {', '.join(sorted(SUPPORTED_TYPES))}")

    destination = Path(output_dir).expanduser() if output_dir else (
        Path.home() / "Documents" / "NavarisOS" / "Generated"
    )
    destination.mkdir(parents=True, exist_ok=True)
    output_path = (destination / f"NAVARIS_{_safe_filename(company_name)}_{type}.xlsx").resolve()

    workbook = Workbook()
    _BUILDERS[type](workbook, company_name.strip())
    workbook.properties.creator = "NAVARIS OS - Private AI"
    workbook.properties.title = f"NAVARIS {type.replace('_', ' ').title()} - {company_name.strip()}"
    workbook.properties.subject = "Private offline consulting workbook"
    workbook.calculation.fullCalcOnLoad = True
    workbook.calculation.forceFullCalc = True
    workbook.save(output_path)
    return output_path
