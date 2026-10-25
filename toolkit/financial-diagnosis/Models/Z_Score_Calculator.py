"""Altman original public-manufacturing Z-score and PDF report.

Use only with the original model's definitions and population. Page 589 is
edition-specific; confirm the user's exact book edition before citing a page.
This is screening, not a credit decision or investment advice.
"""
from pathlib import Path

WEIGHTS = (1.2, 1.4, 3.3, 0.6, 1.0)

def calculate(x1, x2, x3, x4, x5):
    values = (x1, x2, x3, x4, x5)
    if any(not isinstance(v, (int, float)) for v in values):
        raise TypeError("All five ratios must be numeric")
    score = sum(w * x for w, x in zip(WEIGHTS, values))
    return {"z_score": score, "ratios": dict(zip(("X1", "X2", "X3", "X4", "X5"), values)),
            "model": "Altman original Z-score; original public-manufacturing domain only",
            "status": "CALCULATION ONLY; verify definitions, domain and source edition"}

def generate_pdf(result, output="reports/financial-diagnosis.pdf"):
    try:
        from reportlab.lib.pagesizes import A4
        from reportlab.pdfgen import canvas
    except ImportError as exc:
        raise RuntimeError("PDF dependency missing; install reportlab") from exc
    path = Path(output); path.parent.mkdir(parents=True, exist_ok=True)
    pdf = canvas.Canvas(str(path), pagesize=A4)
    pdf.setTitle("NAVARIS Financial Diagnosis — Altman Z-Score")
    lines = ["NAVARIS | Financial Diagnosis", "Altman original Z-score screening", "NOT a credit decision; domain-specific model",
             "Formula: 1.2X1 + 1.4X2 + 3.3X3 + 0.6X4 + 1.0X5",
             *[f"{k}: {v}" for k, v in result["ratios"].items()], f"Z-score: {result['z_score']:.4f}",
             "Verify original variable definitions and applicability before interpretation.",
             "Page 589 is edition-specific; bibliographic edition not independently established."]
    y = 790
    for line in lines:
        pdf.drawString(48, y, line[:115]); y -= 28
    pdf.save(); return path

if __name__ == "__main__":
    result = calculate(0.2, 0.1, 0.08, 1.5, 1.2)
    print(result)
    print(generate_pdf(result))
