"""Generate an illustrative representation-fee scenario PDF; not a real mandate."""
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[3]/"toolkit"/"fund-representation"/"Models"))
from fund_representation_calculator import calculate_retainer

def run():
    total=calculate_retainer(base=2000,success_pct=0.03,deal_value=1000000)
    try:
        from reportlab.lib.pagesizes import A4
        from reportlab.pdfgen import canvas
    except ImportError as exc:
        raise RuntimeError("Install reportlab to generate the PDF: pip install reportlab") from exc
    out=Path(__file__).resolve().parents[3]/"reports"/"fund-representation.pdf"
    out.parent.mkdir(parents=True,exist_ok=True)
    pdf=canvas.Canvas(str(out),pagesize=A4)
    pdf.setTitle("NAVARIS Fund Representation Scenario")
    y=790
    lines=["NAVARIS — Fund & Corporate Representation","ILLUSTRATIVE SCENARIO — NOT A SIGNED MANDATE","Monthly retainer assumption: USD 2,000 (user-provided scenario)","Success-fee assumption: 3% × USD 1,000,000 deal value","Combined first-period scenario: USD "+format(total,",.2f"),"Range of USD 2,000–5,000/month and 2–5% success fee is proposed only.","70/30 ELAFLEX share is unverified; no affiliation or agreement is implied.","Obtain written mandate, compliance review, fee base and payer confirmation."]
    for line in lines:
        pdf.drawString(50,y,line[:115]); y-=28
    pdf.save()
    print(str(out))
    return out
if __name__=="__main__": run()
