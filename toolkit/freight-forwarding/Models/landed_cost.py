"""Landed-cost calculator and reproducible PDF report; inputs are user quotes."""
from pathlib import Path

def calculate(fob, freight, insurance, origin_destination=0, duties_taxes=0, other_fees=0, margin_rate=0):
    costs = {"FOB": fob, "freight": freight, "insurance": insurance,
             "origin_destination": origin_destination, "duties_taxes": duties_taxes, "other_fees": other_fees}
    if any(not isinstance(v, (int, float)) or v < 0 for v in costs.values()):
        raise ValueError("All cost inputs must be non-negative numbers")
    if not isinstance(margin_rate, (int, float)) or margin_rate < 0:
        raise ValueError("margin_rate must be a non-negative decimal")
    total = sum(costs.values())
    return {"inputs": costs, "landed_cost": total, "margin_rate": margin_rate,
            "scenario_sell_price": total * (1 + margin_rate),
            "status": "CALCULATION ONLY; customs, tax and carrier quotes must be verified"}

def generate_pdf(result, output="reports/freight-forwarding-landed-cost.pdf"):
    try:
        from reportlab.lib.pagesizes import A4
        from reportlab.pdfgen import canvas
    except ImportError as exc:
        raise RuntimeError("PDF dependency missing; install reportlab") from exc
    path = Path(output); path.parent.mkdir(parents=True, exist_ok=True)
    pdf = canvas.Canvas(str(path), pagesize=A4); pdf.setTitle("NAVARIS Landed Cost Scenario")
    lines = ["NAVARIS | Freight Forwarding — Landed Cost", "SCENARIO ONLY — based on supplied inputs",
             *[f"{k}: {v:,.2f}" for k, v in result["inputs"].items()],
             f"Landed cost: {result['landed_cost']:,.2f}", f"Margin rate: {result['margin_rate']:.2%}",
             f"Scenario sell price: {result['scenario_sell_price']:,.2f}",
             "ELAFLEX 70/30: proposed commercial split only; requires written agreement.",
             "Exclude no cost silently. Verify Incoterm, HS code, duties, VAT, freight and insurance."]
    y = 790
    for line in lines:
        pdf.drawString(48, y, line[:115]); y -= 28
    pdf.save(); return path

if __name__ == "__main__":
    result = calculate(1000, 150, 10, 30, 0, 20, 0.15)
    print(result); print(generate_pdf(result))
