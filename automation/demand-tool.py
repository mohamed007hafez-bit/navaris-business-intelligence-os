#!/usr/bin/env python3
"""Generate indicative freight scenarios as a valid PDF; these are not carrier offers.
Usage: python automation/demand-tool.py [input.json] [output.pdf]
"""
import json, os, sys
from datetime import date, timedelta
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
NAVY=colors.HexColor("#0A1F44"); GOLD=colors.HexColor("#D4AF37")
# Only user-provided base routes are configured. Unknown routes fail rather than invent a base rate.
ROUTES={("alexandria","jeddah"):2800.0,("alexandria","jebel ali"):3200.0}
CARRIERS=[("MSC",-0.05),("Maersk",0.02),("Hapag-Lloyd",0.10)]
def sample(path):
    os.makedirs(os.path.dirname(path) or ".",exist_ok=True)
    with open(path,"w",encoding="utf-8") as f: json.dump({"origin":"Alexandria","destination":"Jeddah","container_type":"20GP","weight":18000},f,indent=2)
def build(data,out,source):
    origin=str(data.get("origin","")).strip(); dest=str(data.get("destination","")).strip()
    key=(origin.casefold(),dest.casefold())
    if key not in ROUTES: raise ValueError(f"No configured base rate for {origin} → {dest}. Add a verified base rate to ROUTES; no rate was invented.")
    weight=float(data.get("weight",0))
    if weight<=0: raise ValueError("weight must be a positive number (kg)")
    base=ROUTES[key]; fuel=base*.12; peak=base*.08; subtotal=base+fuel+peak; margin=subtotal*.15; total=subtotal+margin
    quotes=[]
    for carrier,variance in CARRIERS: quotes.append({"carrier":carrier,"variance":variance,"total":total*(1+variance)})
    best=min(quotes,key=lambda x:x["total"])
    os.makedirs(os.path.dirname(out) or ".",exist_ok=True)
    st=getSampleStyleSheet(); st.add(ParagraphStyle(name="NavyTitle",parent=st["Title"],textColor=NAVY,fontSize=20))
    doc=SimpleDocTemplate(out,pagesize=A4,rightMargin=18*mm,leftMargin=18*mm,topMargin=16*mm,bottomMargin=16*mm)
    story=[Paragraph("NAVARIS GATEWAY EGYPT — Indicative Freight Scenarios",st["NavyTitle"]),Paragraph("Source file: "+source+" | Generated: "+date.today().isoformat(),st["BodyText"]),Spacer(1,5*mm)]
    summary=[["Origin",origin,"Destination",dest],["Container",str(data.get("container_type","Not supplied")),"Weight",f"{weight:,.0f} kg"],["Configured base rate",f"USD {base:,.2f}","Fuel surcharge (12%)",f"USD {fuel:,.2f}"],["Peak-season assumption (8%)",f"USD {peak:,.2f}","Margin (15%)",f"USD {margin:,.2f}"]]
    t=Table(summary,colWidths=[42*mm,48*mm,42*mm,48*mm]); t.setStyle(TableStyle([("BACKGROUND",(0,0),(0,-1),NAVY),("TEXTCOLOR",(0,0),(0,-1),colors.white),("BACKGROUND",(2,0),(2,-1),NAVY),("TEXTCOLOR",(2,0),(2,-1),colors.white),("GRID",(0,0),(-1,-1),.4,colors.lightgrey),("FONTSIZE",(0,0),(-1,-1),9),("VALIGN",(0,0),(-1,-1),"TOP")]))
    story += [t,Spacer(1,7*mm),Paragraph("Carrier scenario comparison",st["Heading2"])]
    qrows=[["Carrier","Scenario variance","Indicative total (USD)","Basis"]]+[[q["carrier"],f'{q["variance"]:+.0%}',f'{q["total"]:,.2f}',"Modelled scenario; not carrier-confirmed"] for q in quotes]
    qt=Table(qrows,colWidths=[35*mm,35*mm,43*mm,80*mm],repeatRows=1); qt.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,0),NAVY),("TEXTCOLOR",(0,0),(-1,0),colors.white),("GRID",(0,0),(-1,-1),.4,colors.lightgrey),("FONTSIZE",(0,0),(-1,-1),9),("ROWBACKGROUNDS",(0,1),(-1,-1),[colors.white,colors.HexColor("#F3F6FA")])]))
    story += [qt,Spacer(1,5*mm),Paragraph(f"Lowest modelled scenario: {best['carrier']} at USD {best['total']:,.2f}. This is a mathematical scenario only; no carrier API or live tariff was queried.",st["BodyText"]),PageBreak(),Paragraph("Commercial Terms & Assumptions",st["Heading1"])]
    notes=[f"Validity: 14 days, through {(date.today()+timedelta(days=14)).isoformat()}, subject to reconfirmation.", "Incoterms® 2020: select the term only after agreeing delivery point, insurance, export/import clearance and allocation of risk/cost. This scenario does not select an Incoterm or establish a binding offer.", "Drewry World Container Index (WCI) is a market benchmark reference only. No current index value is included because none was retrieved in this script.", "Base rates are hard-coded only for Alexandria–Jeddah (USD 2,800) and Alexandria–Jebel Ali (USD 3,200), as provided in the task. Fuel 12%, peak-season 8%, and margin 15% are user-specified assumptions.", "Carrier variances (MSC −5%, Maersk +2%, Hapag-Lloyd +10%) are illustrative scenario assumptions, not observed carrier pricing.", "Excluded unless verified and added: origin/destination terminal charges, customs, duties, insurance, documentation, demurrage/detention, dangerous-goods surcharges, transshipment and currency risk."]
    for n in notes: story.append(Paragraph("• "+n,st["BodyText"])); story.append(Spacer(1,3*mm))
    story += [Spacer(1,5*mm),Paragraph("NAVARIS | Indicative estimate only — obtain written carrier and customer confirmation before commitment.",st["BodyText"])]
    def footer(c,d):
        c.saveState(); c.setStrokeColor(GOLD); c.line(18*mm,12*mm,192*mm,12*mm); c.setFont("Helvetica",8); c.setFillColor(NAVY); c.drawString(18*mm,7*mm,"NAVARIS | Indicative freight scenario — not a carrier quotation"); c.drawRightString(192*mm,7*mm,f"Page {d.page}"); c.restoreState()
    doc.build(story,onFirstPage=footer,onLaterPages=footer)
    print(f"Created valid PDF: {out} (3 carrier scenarios)")
def main():
    inp=sys.argv[1] if len(sys.argv)>1 else "data/freight.json"; out=sys.argv[2] if len(sys.argv)>2 else "reports/quotes-real.pdf"
    if not os.path.isfile(inp): sample(inp)
    with open(inp,encoding="utf-8") as f: data=json.load(f)
    if not isinstance(data,dict): raise ValueError("Input JSON must be an object.")
    build(data,out,inp)
if __name__=="__main__": main()
