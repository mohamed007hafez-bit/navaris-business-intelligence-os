"""Generate a corporate-stay scenario PDF; lead details are not independently verified."""
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[3]/"toolkit"/"hotel-energy"/"Models"))
from hotel_energy_calculator import corporate_rate

def run():
    rate=corporate_rate()
    try:
        from reportlab.lib.pagesizes import A4
        from reportlab.pdfgen import canvas
    except ImportError as exc:
        raise RuntimeError("Install reportlab to generate the PDF: pip install reportlab") from exc
    out=Path(__file__).resolve().parents[3]/"reports"/"hotel-energy.pdf"
    out.parent.mkdir(parents=True,exist_ok=True)
    pdf=canvas.Canvas(str(out),pagesize=A4)
    pdf.setTitle("NAVARIS Hotel & Energy Rate Scenario")
    y=790
    for line in ["NAVARIS — Hotel & Energy Logistics","SCENARIO ONLY — NOT A VERIFIED OFFER","Rate model scenario (EGP): "+format(rate,".2f"),"Fouad Hotel — user-supplied lead: 15 El Shohadaa St; price range 290–1,000 EGP stated by user; independent source check pending.","Aelat Adaa, Raml Station — user-supplied local lead; name, address, rates and availability not independently verified.","No affiliation, booking, rate, or commission is confirmed. Verify directly before customer use."]:
        pdf.drawString(50,y,line[:115]); y-=28
    pdf.save()
    print(str(out))
    return out
if __name__=="__main__": run()
