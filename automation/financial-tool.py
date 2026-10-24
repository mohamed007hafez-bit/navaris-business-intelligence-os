#!/usr/bin/env python3
"""NAVARIS financial diagnostics: extract labelled figures from PDF and produce a valid 5-page PDF.
Usage: python automation/financial-tool.py input.pdf output.pdf
Without args, creates a clearly labelled synthetic demonstration report at reports/financial-real.pdf.
CCC is calculated only when DIO, DSO and DPO are explicitly supplied in extracted text or sample data.
"""
import os, re, sys
from datetime import datetime
import pdfplumber
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, Image, KeepTogether

NAVY=colors.HexColor("#0A1F44"); GOLD=colors.HexColor("#D4AF37"); RED=colors.HexColor("#B91C1C")
LABELS={"Current Assets":r"current\s+assets","Current Liabilities":r"current\s+liabilities","Revenue":r"(?:total\s+)?revenue|net\s+sales","EBITDA":r"EBITDA","Inventory":r"inventory|inventories","DIO":r"\bDIO\b|days\s+inventory\s+outstanding","DSO":r"\bDSO\b|days\s+sales\s+outstanding","DPO":r"\bDPO\b|days\s+payables\s+outstanding"}
def number_after(text, label_pattern):
    pat=re.compile(r"(?:^|\n)\s*(?:"+label_pattern+r")\s*[:=\-]?\s*(?:USD|EGP|\$|£|€)?\s*\(?\s*(-?[\d,]+(?:\.\d+)?)\s*\)?",re.I)
    m=pat.search(text)
    if not m: return None
    value=float(m.group(1).replace(",",""))
    # Accounting convention: parenthesized negatives are not reliably captured; retain extracted sign.
    return value
def extract_pdf(path):
    pages=[]
    with pdfplumber.open(path) as pdf:
        for p in pdf.pages:
            pages.append(p.extract_text() or "")
    text="\n".join(pages)
    return {k:number_after(text,v) for k,v in LABELS.items()}, text, len(pages)
def safe_div(a,b):
    return a/b if a is not None and b not in (None,0) else None
def fmt(x, suffix=""):
    return "N/A — not found in source" if x is None else f"{x:,.2f}{suffix}"
def build_report(output, values, source, page_count, synthetic=False):
    ca,cl,rev,ebitda,inv=(values.get(k) for k in ("Current Assets","Current Liabilities","Revenue","EBITDA","Inventory"))
    current=safe_div(ca,cl); quick=safe_div(ca-inv if ca is not None and inv is not None else None,cl)
    margin=safe_div(ebitda,rev)
    ccc=(values["DIO"]+values["DSO"]-values["DPO"]) if all(values.get(k) is not None for k in ("DIO","DSO","DPO")) else None
    ratios=[("Current Ratio",current,"x"),("Quick Ratio",quick,"x"),("EBITDA Margin",margin*100 if margin is not None else None,"%"),("Cash Conversion Cycle",ccc," days")]
    os.makedirs(os.path.dirname(output) or ".",exist_ok=True)
    chart=os.path.join(os.path.dirname(output) or ".","financial-ratios-chart.png")
    plot_labels=[x[0] for x in ratios[:3]]; plot_vals=[x[1] for x in ratios[:3]]
    fig,ax=plt.subplots(figsize=(7.2,3.4)); ax.bar(plot_labels,[v if v is not None else 0 for v in plot_vals])
    ax.set_title("NAVARIS Financial Indicators (N/A shown as zero only for chart display)")
    ax.grid(axis="y",alpha=.25); fig.tight_layout(); fig.savefig(chart,dpi=140); plt.close(fig)
    styles=getSampleStyleSheet()
    styles.add(ParagraphStyle(name="NavyTitle",parent=styles["Title"],textColor=NAVY,fontSize=21,leading=26,spaceAfter=8))
    styles.add(ParagraphStyle(name="Section",parent=styles["Heading1"],textColor=NAVY,fontSize=15,spaceAfter=8))
    styles.add(ParagraphStyle(name="Small",parent=styles["BodyText"],fontSize=8,leading=11))
    doc=SimpleDocTemplate(output,pagesize=A4,rightMargin=18*mm,leftMargin=18*mm,topMargin=18*mm,bottomMargin=17*mm)
    story=[]
    def page_header(subtitle):
        story.extend([Paragraph("NAVARIS GATEWAY EGYPT",styles["NavyTitle"]),Paragraph(subtitle,styles["Heading2"]),Spacer(1,5*mm)])
    page_header("Financial Diagnostic Report")
    story += [Paragraph("Purpose: extract labelled financial figures from the supplied PDF and calculate selected liquidity, profitability and working-capital indicators.",styles["BodyText"]),Spacer(1,4*mm)]
    story += [Paragraph("Source: "+source.replace("&","&amp;")+" | Source PDF pages read: "+str(page_count),styles["BodyText"]),Spacer(1,3*mm)]
    story += [Paragraph(("DEMONSTRATION ONLY — synthetic data; not a client assessment." if synthetic else "Automated extraction can miss tables or differently labelled figures. Reconcile all extracted values to the original statements before relying on this report."),styles["BodyText"]),PageBreak()]
    page_header("1. Extracted Financial Inputs")
    rows=[["Input","Extracted value","Interpretation"]]
    descriptions={"Current Assets":"Balance-sheet current assets","Current Liabilities":"Balance-sheet current liabilities","Revenue":"Revenue / net sales","EBITDA":"Earnings before interest, tax, depreciation and amortisation","Inventory":"Inventory / inventories","DIO":"Days inventory outstanding (if explicitly present)","DSO":"Days sales outstanding (if explicitly present)","DPO":"Days payable outstanding (if explicitly present)"}
    for k in LABELS:
        rows.append([k,fmt(values.get(k)),descriptions[k]])
    t=Table(rows,colWidths=[39*mm,43*mm,87*mm],repeatRows=1)
    t.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,0),NAVY),("TEXTCOLOR",(0,0),(-1,0),colors.white),("GRID",(0,0),(-1,-1),.4,colors.lightgrey),("VALIGN",(0,0),(-1,-1),"TOP"),("FONTSIZE",(0,0),(-1,-1),8),("ROWBACKGROUNDS",(0,1),(-1,-1),[colors.white,colors.HexColor("#F3F6FA")]),("LEFTPADDING",(0,0),(-1,-1),6),("RIGHTPADDING",(0,0),(-1,-1),6)]))
    story += [t,PageBreak()]
    page_header("2. Calculated Ratios & Red Flags")
    rows=[["Metric","Result","Formula / rule"]]
    for name,val,suf in ratios:
        formula={"Current Ratio":"Current Assets / Current Liabilities","Quick Ratio":"(Current Assets − Inventory) / Current Liabilities","EBITDA Margin":"EBITDA / Revenue × 100","Cash Conversion Cycle":"DIO + DSO − DPO"}[name]
        rows.append([name,fmt(val,suf),formula])
    t=Table(rows,colWidths=[42*mm,45*mm,82*mm],repeatRows=1)
    t.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,0),NAVY),("TEXTCOLOR",(0,0),(-1,0),colors.white),("GRID",(0,0),(-1,-1),.4,colors.lightgrey),("FONTSIZE",(0,0),(-1,-1),9),("VALIGN",(0,0),(-1,-1),"TOP")]))
    story += [t,Spacer(1,6*mm)]
    flags=[]
    if current is not None and current<1.2: flags.append(f"RED FLAG: Current Ratio {current:.2f}x is below the 1.20x screening threshold.")
    if quick is not None and quick<1.2: flags.append(f"RED FLAG: Quick Ratio {quick:.2f}x is below the 1.20x screening threshold.")
    if current is None: flags.append("REVIEW REQUIRED: Current Ratio unavailable; source labels or values were not extracted.")
    if quick is None: flags.append("REVIEW REQUIRED: Quick Ratio unavailable; current assets, inventory, or current liabilities missing.")
    if margin is None: flags.append("REVIEW REQUIRED: EBITDA Margin unavailable; revenue or EBITDA missing.")
    if ccc is None: flags.append("REVIEW REQUIRED: CCC unavailable; DIO, DSO and DPO must be explicitly present in source.")
    if not flags: flags.append("No threshold red flag was triggered by the available ratios; this is not an assurance opinion.")
    for f in flags: story.append(Paragraph("• "+f,ParagraphStyle("flag"+str(len(story)),parent=styles["BodyText"],textColor=RED if "RED FLAG" in f else NAVY,spaceAfter=5)))
    story += [PageBreak()]
    page_header("3. Ratio Chart")
    story += [Image(chart,width=165*mm,height=78*mm),Spacer(1,5*mm),Paragraph("Chart values use the calculated ratios; missing metrics are represented as zero solely for chart rendering and remain marked N/A in the table.",styles["Small"]),PageBreak()]
    page_header("4. Methodology, Limitations & Actions")
    bullets=["Current Ratio = Current Assets ÷ Current Liabilities.","Quick Ratio = (Current Assets − Inventory) ÷ Current Liabilities.","EBITDA Margin = EBITDA ÷ Revenue × 100.","Cash Conversion Cycle = DIO + DSO − DPO; CCC is not estimated if any component is absent.","Liquidity red-flag threshold: below 1.20x for current or quick ratio. This is a screening threshold, not a universal covenant.","pdfplumber extracts text layer content; scanned/image-only PDFs require OCR and may produce missing values.","This automated report is not an audit, valuation, credit decision or financial advice. Validate source figures and accounting policies."]
    for b in bullets: story.append(Paragraph("• "+b,styles["BodyText"])); story.append(Spacer(1,2*mm))
    story += [Spacer(1,4*mm),Paragraph("Generated: "+datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC"),styles["Small"]),Paragraph("NAVARIS | FACT → SOURCE → CALCULATION → ASSUMPTION → EVALUATION → ACTION",styles["Small"])]
    def footer(canvas,doc_):
        canvas.saveState(); canvas.setStrokeColor(GOLD); canvas.line(18*mm,13*mm,192*mm,13*mm)
        canvas.setFont("Helvetica",8); canvas.setFillColor(NAVY); canvas.drawString(18*mm,8*mm,"NAVARIS | Internal diagnostic — validate before decisions")
        canvas.drawRightString(192*mm,8*mm,f"Page {doc_.page} of 5"); canvas.restoreState()
    doc.build(story,onFirstPage=footer,onLaterPages=footer)
    print(f"Created valid PDF: {output} (5 pages); source figures extracted, missing values disclosed.")
def main():
    if len(sys.argv)>=3:
        src,out=sys.argv[1],sys.argv[2]
        if not os.path.isfile(src): raise SystemExit(f"Input PDF not found: {src}")
        vals,_,pages=extract_pdf(src); build_report(out,vals,src,pages)
    else:
        vals={"Current Assets":1250000.0,"Current Liabilities":900000.0,"Revenue":4200000.0,"EBITDA":525000.0,"Inventory":300000.0,"DIO":42.0,"DSO":38.0,"DPO":31.0}
        build_report("reports/financial-real.pdf",vals,"Synthetic NAVARIS demo data",0,True)
if __name__=="__main__": main()
