#!/usr/bin/env python3
"""Score supplier CSVs and generate a valid PDF evaluation report.
Usage: python automation/supplier-tool.py [input.csv] [output.pdf]
If the CSV is absent, a clearly labelled demo CSV is created.
"""
import csv, os, sys
from datetime import date
from dateutil.relativedelta import relativedelta
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
REQUIRED=["supplier_name","technical_score","commercial_score","compliance_score","country","iso_cert"]
NAVY=colors.HexColor("#0A1F44"); GOLD=colors.HexColor("#D4AF37")
def sample(path):
    os.makedirs(os.path.dirname(path) or ".",exist_ok=True)
    with open(path,"w",newline="",encoding="utf-8") as f:
        w=csv.DictWriter(f,fieldnames=REQUIRED); w.writeheader()
        w.writerows([
          {"supplier_name":"Test Supplier","technical_score":85,"commercial_score":78,"compliance_score":90,"country":"Egypt","iso_cert":"ISO 9001"},
          {"supplier_name":"Demo Industrial Co","technical_score":92,"commercial_score":88,"compliance_score":95,"country":"UAE","iso_cert":"ISO 9001"},
          {"supplier_name":"Sample Parts Ltd","technical_score":62,"commercial_score":58,"compliance_score":70,"country":"China","iso_cert":"Not supplied"}])
def load(path):
    with open(path,newline="",encoding="utf-8-sig") as f:
        reader=csv.DictReader(f)
        missing=[x for x in REQUIRED if x not in (reader.fieldnames or [])]
        if missing: raise ValueError("Missing required CSV columns: "+", ".join(missing))
        result=[]
        for n,row in enumerate(reader,2):
            scores=[float(row[k]) for k in REQUIRED[1:4]]
            if any(x<0 or x>100 for x in scores): raise ValueError(f"Line {n}: scores must be 0–100")
            total=scores[0]*.4+scores[1]*.3+scores[2]*.3
            strategic=scores[0]>80 and scores[1]>80
            status="Green" if total>=80 else ("Amber" if total>=60 else "Red")
            result.append({"name":row["supplier_name"],"tech":scores[0],"commercial":scores[1],"compliance":scores[2],"country":row["country"],"iso":row["iso_cert"],"total":total,"category":"Strategic" if strategic else "Non-strategic / review","status":status,"expiry":(date.today()+relativedelta(months=12)).isoformat()})
        return result
def build(rows,out,source):
    os.makedirs(os.path.dirname(out) or ".",exist_ok=True)
    st=getSampleStyleSheet(); st.add(ParagraphStyle(name="NavyTitle",parent=st["Title"],textColor=NAVY,fontSize=20))
    doc=SimpleDocTemplate(out,pagesize=landscape(A4),rightMargin=12*mm,leftMargin=12*mm,topMargin=14*mm,bottomMargin=14*mm)
    story=[Paragraph("NAVARIS GATEWAY EGYPT — Supplier Qualification",st["NavyTitle"]),Paragraph("Source: "+source+" | Generated: "+date.today().isoformat(),st["BodyText"]),Spacer(1,5*mm)]
    data=[["Supplier","Country","Tech 40%","Commercial 30%","Compliance 30%","Total","Status","Kraljic screen","ISO evidence","Review expiry"]]
    for r in rows: data.append([r["name"],r["country"],f'{r["tech"]:.1f}',f'{r["commercial"]:.1f}',f'{r["compliance"]:.1f}',f'{r["total"]:.1f}',r["status"],r["category"],r["iso"],r["expiry"]])
    t=Table(data,colWidths=[32*mm,18*mm,18*mm,22*mm,22*mm,15*mm,17*mm,29*mm,25*mm,23*mm],repeatRows=1)
    commands=[("BACKGROUND",(0,0),(-1,0),NAVY),("TEXTCOLOR",(0,0),(-1,0),colors.white),("GRID",(0,0),(-1,-1),.4,colors.lightgrey),("FONTSIZE",(0,0),(-1,-1),7),("VALIGN",(0,0),(-1,-1),"TOP"),("ROWBACKGROUNDS",(0,1),(-1,-1),[colors.white,colors.HexColor("#F3F6FA")])]
    for i,r in enumerate(rows,1):
        if r["status"]=="Red": commands.append(("TEXTCOLOR",(6,i),(6,i),colors.red))
        elif r["status"]=="Green": commands.append(("TEXTCOLOR",(6,i),(6,i),colors.HexColor("#15803D")))
        else: commands.append(("TEXTCOLOR",(6,i),(6,i),colors.HexColor("#B45309")))
    t.setStyle(TableStyle(commands)); story += [t,Spacer(1,7*mm),Paragraph("Methodology",st["Heading2"])]
    notes=["Weighted score = technical × 0.40 + commercial × 0.30 + compliance × 0.30; each input is scored 0–100.","Status: Green ≥80; Amber ≥60 and <80; Red <60.","Kraljic screen: suppliers with technical score >80 AND commercial score >80 are flagged Strategic for further portfolio/risk review. This is a simplified screening rule, not the full Kraljic matrix (which also requires supply risk and profit impact).","ISO 9001 certificate field is recorded as supplied evidence only; certificate authenticity, scope and expiry have not been independently verified. Review expiry is scheduled 12 months from report date, not the certificate expiry.","Use supplier due diligence, sanctions checks, references, technical validation and commercial terms before award."]
    for n in notes: story.append(Paragraph("• "+n,st["BodyText"])); story.append(Spacer(1,2*mm))
    def footer(c,d):
        c.saveState(); c.setStrokeColor(GOLD); c.line(12*mm,10*mm,285*mm,10*mm); c.setFont("Helvetica",7); c.setFillColor(NAVY); c.drawString(12*mm,5*mm,"NAVARIS | Supplier screening — verify documents independently"); c.drawRightString(285*mm,5*mm,f"Page {d.page}"); c.restoreState()
    doc.build(story,onFirstPage=footer,onLaterPages=footer)
    print(f"Created valid PDF: {out} ({len(rows)} suppliers)")
def main():
    inp=sys.argv[1] if len(sys.argv)>1 else "data/suppliers.csv"; out=sys.argv[2] if len(sys.argv)>2 else "reports/suppliers-real.pdf"
    if not os.path.isfile(inp): sample(inp)
    rows=load(inp)
    if not rows: raise SystemExit("Supplier CSV has headers but no supplier rows.")
    build(rows,out,inp)
if __name__=="__main__": main()
