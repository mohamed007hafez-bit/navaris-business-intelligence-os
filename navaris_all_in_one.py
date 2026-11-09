"""NAVARIS Business Intelligence OS — single-message Streamlit experience.

Run with: streamlit run navaris_all_in_one.py
All outputs are deterministic planning scenarios. No external research is run and no
market, property, supplier, regulatory, financial, or contractual fact is verified here.
"""
from __future__ import annotations

import html
import math
import re
from datetime import datetime
from typing import Any

import streamlit as st

DEFAULT_CAPITAL = 2_000_000.0
DEFAULT_CURRENCY = "EGP"
DISCOUNT_RATE = 0.20  # Explicit illustrative planning assumption; not a market rate.
PROJECTS = [
    ("🏨 Fouad - Miramar", "Fouad - Miramar"),
    ("🚢 Supply Vessel 50m - NOVCC", "Supply Vessel 50m - NOVCC"),
    ("🏛️ Adada - Heritage", "Adada - Heritage"),
]
SOPS_DB = {
    "Fouad": [
        "Confirm property identity, authorization, availability and written rate directly.",
        "Capture client dates, room requirements, inclusions and cancellation terms.",
        "Obtain and compare written supplier quotations; record taxes and exclusions.",
        "Confirm booking authority and payment/commission terms before any commitment.",
        "Reconcile booking confirmation, guest changes, invoice and close-out evidence.",
    ],
    "Adada": [
        "Confirm site identity, ownership/authority, heritage status and access permissions.",
        "Document visitor experience, capacity, operating constraints and conservation needs.",
        "Validate demand, licensing, partner roles, costs and a reversible pilot before launch.",
    ],
    "Customs": [
        "Confirm HS classification and current requirements with a licensed customs professional.",
        "Collect invoice, packing list, origin, permits and shipment documents.",
        "Verify duty, tax, inspection and clearance costs against dated official evidence.",
        "Reconcile declarations, releases, charges and delivery proof.",
    ],
    "Warehouse": [
        "Verify inbound booking, receiving documents and expected quantities.",
        "Inspect and record quantity, condition, lot/serial and discrepancies.",
        "Post authorized movements and maintain location-level inventory records.",
    ],
    "Slickline": [
        "Confirm written scope, well/site, programme, schedule and authorized operator contact.",
        "Verify execution-partner competence, equipment certifications and HSE documents.",
        "Coordinate crew/equipment readiness and approved mobilization documents.",
        "Record daily progress, changes, incidents and client approvals.",
        "Complete service report, close-out evidence and invoice reconciliation.",
    ],
    "Ship Charter": [
        "Confirm cargo/service scope, route, dates, vessel requirements and decision authority.",
        "Verify vessel particulars, class, insurance, flag and relevant certificates.",
        "Collect and compare written owner/operator offers and exclude unsupported rates.",
        "Review charter terms, laytime, demurrage, cancellation and applicable clauses.",
        "Obtain human/legal approval before fixture, commitment or external confirmation.",
    ],
}
SOURCES = [
    "[Minto] Barbara Minto, The Pyramid Principle (method reference; edition/page to verify).",
    "[BIMCO SUPPLYTIME 2017] BIMCO SUPPLYTIME 2017 (contract reference; applicability and current text require legal review).",
    "[IMO SOLAS] IMO SOLAS (safety reference; applicable requirements depend on vessel and voyage).",
    "[DNV] DNV rules/standards (verify applicable edition and scope).",
    "[ISO 9001:2015] ISO 9001:2015 (QMS reference; NAVARIS does not certify).",
    "[SLB] SLB (company reference only; no endorsement or source-specific claim asserted).",
    "[Booking] Booking.com (property/rate/availability must be checked directly; no affiliation asserted).",
    "[CBE USD 48.10] User-provided scenario assumption only; not a verified/current CBE rate.",
]


def _normalize_digits(text: str) -> str:
    return text.translate(str.maketrans("٠١٢٣٤٥٦٧٨٩۰۱۲۳۴۵۶۷۸۹", "01234567890123456789"))


def detect_inputs(message: str) -> dict[str, Any]:
    text = _normalize_digits(message)
    lower = text.lower()
    capital = DEFAULT_CAPITAL
    match = re.search(r"(?:capital|budget|investment|رأس\s*المال|ميزانية)?\s*([\d][\d,]*(?:\.\d+)?)\s*(million|mn|مليون|م)?", lower)
    if match:
        try:
            capital = float(match.group(1).replace(",", ""))
            if match.group(2) in ("million", "mn", "مليون", "م"):
                capital *= 1_000_000
        except ValueError:
            capital = DEFAULT_CAPITAL
    currency = "USD" if re.search(r"\b(?:usd|\$|dollar)\b", lower) else "EUR" if re.search(r"\b(?:eur|€|euro)\b", lower) else "EGP"
    if re.search(r"فؤاد|fouad|miramar|hotel|فندق", lower):
        sector, subtype, sop_key = "Hospitality", "Hotel / corporate stays", "Fouad"
        diagnosis = "Hospitality opportunity identified. Property identity, Miramar association, rates, availability, permissions and client demand are unverified; validate directly before offering or booking."
    elif re.search(r"adada|heritage|ادادا|تراث", lower):
        sector, subtype, sop_key = "Tourism & heritage", "Heritage experience", "Adada"
        diagnosis = "Heritage/tourism concept identified. Site identity, rights, conservation constraints, licensing, demand and operating partners need evidence and human review."
    elif re.search(r"vessel|ship|charter|novcc|supply|سفينة|سفينة", lower):
        sector, subtype, sop_key = "Maritime", "Vessel charter / NVOCC-related planning", "Ship Charter"
        diagnosis = "Maritime opportunity identified. A 50 m vessel and NVOCC role are user-described inputs, not verified capability or vessel particulars. Confirm authority, vessel documents, cargo/service scope, route and written offers."
    elif re.search(r"slickline|wireline|well|oilfield|سليكلاين", lower):
        sector, subtype, sop_key = "Oilfield services", "Slickline / well coordination", "Slickline"
        diagnosis = "Oilfield coordination opportunity identified. Confirm client mandate, site/scope, execution partner, HSE, certificates and schedule; no field execution or mobilization is guaranteed."
    elif re.search(r"custom|جمارك", lower):
        sector, subtype, sop_key = "Trade logistics", "Customs coordination", "Customs"
        diagnosis = "Customs/logistics need identified. Classification, duties, permits and clearance requirements must be verified with current official sources and an authorized professional."
    elif re.search(r"warehouse|مخزن", lower):
        sector, subtype, sop_key = "Logistics", "Warehouse operations", "Warehouse"
        diagnosis = "Warehouse operations opportunity identified. Validate volumes, site capability, inventory controls, service levels and client evidence before committing."
    else:
        sector, subtype, sop_key = "Business project", "General feasibility", "Customs"
        diagnosis = "General business project identified. The message does not establish a validated sector, customer, demand, supplier, cost or revenue; treat this as an initial screening only."
    return {"sector": sector, "subtype": subtype, "sop_key": sop_key, "capital": max(0.0, capital), "currency": currency, "diagnosis": diagnosis}


def finance_metrics(capital: float) -> dict[str, Any]:
    """Illustrative same-formula NPV / IRR / payback / BCR scenario, not a forecast."""
    # Transparent placeholder cash flows make the requested metrics computable without
    # pretending that project-specific revenues or costs were supplied.
    cash_flows = [-capital, capital * 0.25, capital * 0.35, capital * 0.45]
    npv = sum(cf / ((1 + DISCOUNT_RATE) ** year) for year, cf in enumerate(cash_flows))
    lo, hi = -0.9999, 10.0
    for _ in range(250):
        mid = (lo + hi) / 2
        value = sum(cf / ((1 + mid) ** year) for year, cf in enumerate(cash_flows))
        if value > 0:
            lo = mid
        else:
            hi = mid
    irr = (lo + hi) / 2
    annual_cash = cash_flows[1:]
    cumulative, payback = 0.0, None
    for year, flow in enumerate(annual_cash, 1):
        if cumulative + flow >= capital:
            payback = year - 1 + (capital - cumulative) / flow if flow > 0 else None
            break
        cumulative += flow
    pv_benefits = sum(cf / ((1 + DISCOUNT_RATE) ** year) for year, cf in enumerate(cash_flows) if year and cf > 0)
    pv_costs = capital
    return {"npv": npv, "irr": irr, "payback": payback, "bcr": pv_benefits / pv_costs if pv_costs else None, "cash_flows": cash_flows}


def create_report(message: str) -> dict[str, Any]:
    details = detect_inputs(message)
    metrics = finance_metrics(details["capital"])
    is_hormuz_closed = bool(re.search(r"hormuz\s*(?:is\s*)?closed|مضيق هرمز مغلق", message, re.I))
    # OTIF is unknown unless supplied; never invent a performance reading.
    otif_match = re.search(r"otif\s*[:=<>]?\s*(\d+(?:\.\d+)?)\s*%?", message, re.I)
    otif = float(otif_match.group(1)) if otif_match else None
    score = 72 if details["sector"] != "Business project" else 58
    return {"message": message, **details, "finance": metrics, "score": score,
            "otif": otif, "hormuz_closed": is_hormuz_closed,
            "alert": "🔴 CRITICAL — Hormuz marked CLOSED in user input; verify current route conditions." if is_hormuz_closed else "🔴 Alert — OTIF below 85%." if otif is not None and otif < 85 else "No threshold alert; OTIF / route status not independently verified.",
            "created": datetime.now().strftime("%Y-%m-%d %H:%M")}


def money(value: float, currency: str) -> str:
    return f"{currency} {value:,.0f}"


def one_pager(report: dict[str, Any]) -> str:
    f = report["finance"]
    npv = "NOT CALCULABLE" if f["npv"] is None else money(f["npv"], report["currency"])
    irr = "NOT CALCULABLE" if f["irr"] is None else f"{f['irr']:.1%}"
    payback = "NOT CALCULABLE" if f["payback"] is None else f"{f['payback']:.2f} years"
    return f"""# NAVARIS — Fund One-Pager\n\n**Project:** {report['message']}  \n**Screening date:** {report['created']}  \n**Sector / sub-sector:** {report['sector']} / {report['subtype']}  \n**Planning capital:** {money(report['capital'], report['currency'])} (default if not supplied)\n\n## Investment snapshot\n- **Diagnosis:** {report['diagnosis']}\n- **Illustrative NPV:** {npv}\n- **Illustrative IRR:** {irr}\n- **Illustrative payback:** {payback}\n- **Illustrative BCR:** {f['bcr']:.2f}x\n- **Readiness score:** {report['score']}/100 — heuristic screening score, not diligence or credit approval\n- **Radar:** {report['alert']}\n\n## Financial assumptions & limitations\nScenario-only annual net cash flows are -capital, 25%, 35%, and 45% of capital in years 1–3; discount rate is an illustrative 20%. Replace with dated, evidenced cash flows, taxes, fees, working capital and a justified cost of capital. No project revenue, cost, market rate, source, demand, asset, regulatory status or return is verified. This is not investment, legal, tax or financial advice.\n\n## Immediate diligence gates\n1. Validate buyer need, authority, demand and source evidence.\n2. Obtain written supplier/partner quotes, scope, liabilities and delivery capability.\n3. Rebuild the model from evidenced project cash flows and stress cases.\n4. Legal/compliance review and human approval before any external offer, contract or commitment.\n\n## References supplied for screening\n" + "\\n".join("- " + s for s in SOURCES) + "\n"""


def render_report(report: dict[str, Any]) -> None:
    st.markdown(f"<div class='user-bubble'>{html.escape(report['message'])}</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='meta-line'>{report['sector']} <span>·</span> {report['subtype']} <span>·</span> Planning capital {money(report['capital'], report['currency'])} <span>·</span> Currency {report['currency']}</div>", unsafe_allow_html=True)
    st.markdown("<div class='agent-card'><div class='agent-title'>🔍 &nbsp;ResearchAgent <span class='done'>Done</span></div><div class='agent-body'><b>Diagnosis</b><br>" + html.escape(report["diagnosis"]) + "<br><br><b>Method:</b> Minto Pyramid + MECE-style structuring. This is desk-screening text, not live research or verified evidence.<br><br><b>References</b><br>" + "<br>".join(html.escape(s) for s in SOURCES) + "</div></div>", unsafe_allow_html=True)
    f = report["finance"]
    npv_color = "positive" if f["npv"] >= 0 else "negative"
    irr_text = f"{f['irr']:.1%}" if f["irr"] is not None else "NOT CALCULABLE"
    payback_text = f"{f['payback']:.2f} yr" if f["payback"] is not None else "NOT CALCULABLE"
    st.markdown("<div class='agent-card'><div class='agent-title'>💰 &nbsp;FinancialAgent <span class='done'>Done</span></div><div class='agent-body'>Illustrative scenario only — not project-specific forecast.<div class='metric-row'><div class='metric'><small>NPV @ 20% assumed</small><b class='" + npv_color + "'>" + money(f["npv"], report["currency"]) + "</b></div><div class='metric'><small>IRR</small><b>" + irr_text + "</b></div><div class='metric'><small>Payback</small><b>" + payback_text + "</b></div></div><div class='small-note'>BCR: " + (f"{f['bcr']:.2f}x" if f["bcr"] is not None else "NOT CALCULABLE") + " · Formula: NPV = Σ CFₜ/(1+r)ᵗ − initial investment. IRR solves NPV=0. Assumed cash flows: -capital; +25%, +35%, +45% in years 1–3. These must be replaced with evidenced figures.</div></div></div>", unsafe_allow_html=True)
    sop_list = SOPS_DB[report["sop_key"]]
    with st.expander(f"📋 SOPsAgent · {len(sop_list)} SOPs", expanded=False):
        for i, item in enumerate(sop_list, 1):
            st.markdown(f"**{i}.** {item}")
    st.markdown("<div class='agent-card'><div class='agent-title'>📜 &nbsp;ContractAgent <span class='done'>Done</span></div><div class='agent-body'><b>Proposed asset-light structure:</b> DEMAND &lt; NAVARIS &gt; SUPPLIER. NAVARIS coordinates only within a written, authorized mandate; demand and supplier remain separately responsible for their obligations.<br><br><b>Commercial term for review:</b> 50% advance, subject to signed scope and written agreement. Include force-majeure and route disruption provisions covering Hormuz / Bab El-Mandeb where relevant, with notice, mitigation, suspension and termination mechanics.<br><br><span class='small-note'>Drafting prompt only — not a contract or legal advice. BIMCO SUPPLYTIME 2017 is not automatically suitable; obtain qualified legal review and human approval.</span></div></div>", unsafe_allow_html=True)
    radar = html.escape(report["alert"])
    otif = f"{report['otif']:.1f}%" if report["otif"] is not None else "Unknown — no value supplied"
    st.markdown("<div class='agent-card'><div class='agent-title'>📈 &nbsp;DashboardAgent + RadarAgent <span class='done'>Done</span></div><div class='agent-body'><div class='metric-row'><div class='metric'><small>Screening score</small><b>" + str(report["score"]) + "/100</b></div><div class='metric'><small>OTIF</small><b>" + otif + "</b></div></div><br><b>Radar:</b> " + radar + "<div class='small-note'>Score is a simple heuristic based on sector classification, not a validated rating. Alert rule: OTIF &lt;85% or user reports Hormuz CLOSED. Statuses are not independently monitored.</div></div></div>", unsafe_allow_html=True)
    st.download_button("📄 Download One-Pager", data=one_pager(report), file_name="navaris-fund-one-pager.md", mime="text/markdown", key=f"download_{report['created']}_{abs(hash(report['message']))}")


def init_state() -> None:
    for key, value in {"active_report": None, "history": [], "chat_input": "", "notice": ""}.items():
        if key not in st.session_state:
            st.session_state[key] = value


def apply_link_actions() -> None:
    params = st.query_params
    if "project" in params:
        st.session_state.chat_input = str(params["project"])
        st.query_params.clear()
    elif "history" in params:
        try:
            index = int(params["history"])
            if 0 <= index < len(st.session_state.history):
                st.session_state.active_report = st.session_state.history[index]
                st.session_state.chat_input = ""
        except (ValueError, TypeError):
            pass
        st.query_params.clear()


def main() -> None:
    st.set_page_config(page_title="NAVARIS · Business Intelligence OS", page_icon="◈", layout="wide", initial_sidebar_state="expanded")
    init_state()
    apply_link_actions()
    st.markdown("""<style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Manrope:wght@500;600;700;800&display=swap');
    :root{--bg:#F7F5F0;--navy:#0A1F44;--gold:#C9A86A;--ink:#17243a;--muted:#758095;--line:#ece9e2}
    .stApp{background:var(--bg);color:var(--ink);font-family:'DM Sans',sans-serif}.block-container{max-width:980px;padding-top:1.6rem;padding-bottom:3rem}
    [data-testid="stSidebar"]{background:#fff;border-right:1px solid var(--line)}[data-testid="stSidebar"] .block-container{padding-top:1.6rem}
    .brand{display:flex;align-items:center;gap:12px;padding:4px 0 24px;color:var(--navy)}.brand-mark{width:38px;height:38px;border:1px solid #dcd5c7;border-radius:13px;display:grid;place-items:center;font-family:Manrope;font-weight:800;font-size:19px}.brand-name{font-family:Manrope;font-weight:800;letter-spacing:.15em;font-size:14px}.brand-sub{font-size:11px;color:var(--muted);margin-top:2px}
    .topbrand{display:flex;align-items:center;gap:10px;color:var(--navy);font-size:12px;font-weight:700;letter-spacing:.02em;margin:0 0 56px}.topbrand .logo{font-family:Manrope;font-weight:800;letter-spacing:.16em;font-size:14px;border:1px solid #e6e1d7;border-radius:10px;padding:8px 11px;background:#fff}.hero{text-align:center;margin:0 auto 24px}.eyebrow{font-size:10px;letter-spacing:.2em;color:#9b8a69;text-transform:uppercase;font-weight:700}.hero h1{font-family:Manrope;color:var(--navy);font-size:30px;line-height:1.25;margin:10px 0 9px}.hero p{font-size:14px;color:var(--muted);margin:0}
    .stTextArea textarea{border:1px solid #e6e2d9!important;border-radius:20px!important;background:#fff!important;padding:21px!important;min-height:145px!important;font-size:16px!important;line-height:1.65!important;color:var(--navy)!important;box-shadow:0 8px 28px rgba(10,31,68,.035)}.stTextArea textarea:focus{border-color:#c9a86a!important;box-shadow:0 0 0 1px #c9a86a!important}
    .chips{display:flex;gap:9px;justify-content:center;flex-wrap:wrap;margin:8px 0 17px}.chip{display:inline-block;text-decoration:none!important;color:#42516a!important;background:#fff;border:1px solid #e9e5dc;border-radius:999px;padding:8px 13px;font-size:12px;font-weight:600;transition:.18s}.chip:hover{border-color:#c9a86a;color:#0A1F44!important;transform:translateY(-1px)}
    .stForm{border:0}.stForm [data-testid="stForm"]{border:0;padding:0}.stFormSubmitButton button{background:#C9A86A!important;color:#0A1F44!important;border:0!important;border-radius:13px!important;font-weight:700!important;padding:10px 25px!important;min-height:45px}.stFormSubmitButton button:hover{background:#b9975c!important}.stButton button{border-radius:10px!important;border:1px solid #e8e4dc!important;color:#0A1F44!important;background:#fff!important;font-weight:600!important}.stButton button:hover{border-color:#c9a86a!important}
    .agent-card{background:#fff;border:1px solid #efede7;border-radius:22px;padding:21px 23px;margin:17px 0;box-shadow:0 8px 28px rgba(10,31,68,.035)}.agent-title{font-family:Manrope;font-size:15px;font-weight:700;color:var(--navy);display:flex;align-items:center;gap:6px}.done{margin-left:auto;font-family:'DM Sans';font-size:10px;color:#427b64;background:#edf6f0;padding:5px 9px;border-radius:99px}.agent-body{font-size:13px;line-height:1.75;color:#49566a;margin-top:13px}.metric-row{display:flex;gap:10px;margin-top:14px}.metric{flex:1;background:#faf9f6;border:1px solid #f0eee8;border-radius:15px;padding:13px}.metric small{display:block;color:#828b99;font-size:10px;margin-bottom:5px}.metric b{font-family:Manrope;color:var(--navy);font-size:17px}.metric b.positive{color:#2c7960}.metric b.negative{color:#b24b47}.small-note{font-size:11px;color:#828b99;line-height:1.65;margin-top:12px}.user-bubble{background:#0A1F44;color:white;padding:13px 17px;border-radius:18px 18px 5px 18px;max-width:80%;margin:12px 0 8px auto;width:fit-content}.meta-line{text-align:right;font-size:11px;color:#7a8492;margin-bottom:15px}.meta-line span{padding:0 5px;color:#c9a86a}
    [data-testid="stExpander"]{background:#fff;border:1px solid #efede7;border-radius:18px!important;overflow:hidden}[data-testid="stExpander"] summary{font-weight:700;color:var(--navy)}.sidebar-label{font-size:10px;text-transform:uppercase;letter-spacing:.16em;color:#9a8b70;font-weight:700;margin:22px 0 9px}.history-link{display:block;color:#59667a;text-decoration:none;padding:9px 10px;border-radius:9px;font-size:12px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}.history-link:hover{background:#f7f5f0;color:#0A1F44}.footer-note{text-align:center;color:#9aa1ab;font-size:10px;margin:30px 0 0}
    </style>""", unsafe_allow_html=True)
    with st.sidebar:
        st.markdown("<div class='brand'><div class='brand-mark'>N</div><div><div class='brand-name'>NAVARIS</div><div class='brand-sub'>Business Intelligence OS</div></div></div>", unsafe_allow_html=True)
        if st.button("＋  New Chat", use_container_width=True, key="new_chat"):
            current = st.session_state.active_report
            if current:
                st.session_state.history.insert(0, current)
                st.session_state.history = st.session_state.history[:5]
            st.session_state.active_report = None
            st.session_state.chat_input = ""
            st.rerun()
        st.markdown("<div class='sidebar-label'>Recent chats</div>", unsafe_allow_html=True)
        for i, old in enumerate(st.session_state.history[:5]):
            label = html.escape(old["message"][:35] or old["sector"])
            st.markdown(f"<a class='history-link' href='?history={i}' title='{label}'>◦ &nbsp;{label}</a>", unsafe_allow_html=True)
        if not st.session_state.history:
            st.markdown("<div style='font-size:12px;color:#9aa1ab;padding:8px 10px'>Your recent chats will appear here.</div>", unsafe_allow_html=True)
    st.markdown("<div class='topbrand'><span class='logo'>NAVARIS</span><span>Business Intelligence OS</span></div>", unsafe_allow_html=True)
    if st.session_state.active_report:
        st.markdown("<div class='hero'><div class='eyebrow'>One message · coordinated intelligence</div><h1>Your project, clearly understood.</h1><p>Five specialist agents prepare a concise, evidence-aware project screen.</p></div>", unsafe_allow_html=True)
        render_report(st.session_state.active_report)
        st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)
    else:
        st.markdown("<div class='hero'><div class='eyebrow'>One message · coordinated intelligence</div><h1>What are you building?</h1><p>Describe a project in one message. NAVARIS will organize the first-pass analysis.</p></div>", unsafe_allow_html=True)
    with st.form("one_message_form", clear_on_submit=False, border=False):
        message = st.text_area("Project description", key="chat_input", label_visibility="collapsed", placeholder="اكتب مشروعك هنا... مثال: فندق فؤاد - Miramar - أو Supply Vessel 50m - NOVCC", height=145)
        st.markdown("<div class='chips'>" + "".join(f"<a class='chip' href='?project={html.escape(value, quote=True)}'>{html.escape(label)}</a>" for label, value in PROJECTS) + "</div>", unsafe_allow_html=True)
        sent = st.form_submit_button("Send  ↗", use_container_width=True)
    if sent:
        if not message.strip():
            st.warning("اكتب وصف المشروع أولاً — Please describe your project first.")
        else:
            old = st.session_state.active_report
            if old and old["message"] != message.strip():
                st.session_state.history.insert(0, old)
                st.session_state.history = st.session_state.history[:5]
            report = create_report(message.strip())
            st.session_state.active_report = report
            st.rerun()
    if st.session_state.notice:
        st.info(st.session_state.notice)
        st.session_state.notice = ""
    st.markdown("<div class='footer-note'>Planning support only · Verify sources, assumptions, terms and regulatory requirements before acting.</div>", unsafe_allow_html=True)


if __name__ == "__main__":
    main()
