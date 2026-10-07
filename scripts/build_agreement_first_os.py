from openpyxl import load_workbook
from openpyxl.styles import Font,Alignment
from openpyxl.utils import get_column_letter
from pathlib import Path
p=Path("data/NAVARIS_3Part_AgreementFirst_OS.xlsx"); w=load_workbook(p)
for s in ["OPPORTUNITY_MAP","TOOLKIT","OEM_OILFIELD","OEM_MARITIME"]:
    if s in w.sheetnames: del w[s]
def rows(s): return [x.split("|") for x in s.strip().splitlines()]
def ws(name,h,r):
    q=w.create_sheet(name); q.append(h)
    for x in r:q.append(x)
    for c in q[1]: c.font=Font(bold=True)
    for z in q.iter_rows():
        for c in z:c.alignment=Alignment(wrap_text=True,vertical="top")
    q.freeze_panes="A2";q.auto_filter.ref=q.dimensions
    for i in range(1,q.max_column+1):q.column_dimensions[get_column_letter(i)].width=min(42,max(12,max(len(str(q.cell(j,i).value or "")) for j in range(1,q.max_row+1))+2))
op=rows("""A1|EGPC Emergency Parts|Critical emergency/maintenance spares; exact RFQ/model verify|Emergency Sourcing / Deal Support|EGPC / petroleum operators|Emergency sourcing fee / margin|Immediate / case-dependent|Verify RFQ, part number, buyer and supplier route
A2|EGAS Gas Exploration|Exploration/project equipment demand; package verify|Sourcing + Tender Readiness|EGAS / contractors|Sourcing fee / commission|Near-term / case-dependent|Map live opportunity and vendor route
A3|EDC Drilling|Drilling/workover equipment and operational support|Diagnostic + Sourcing|Egyptian Drilling Company|Project fee + sourcing margin|Near-term / case-dependent|Qualify equipment gap and OEM alternatives
A4|ECMR Gold Mining|Mining technology, production and supply-chain demand|Diagnostic + Commercial Rep|ECMR / mining contractors|Diagnostic fee + commission|Near-term / case-dependent|Identify active project and package
A5|Suez Canal Emergency|Critical marine spare/repair need; exact need verify|Emergency Marine Sourcing|Suez Canal ecosystem / vessel operators|Supplier margin|Immediate / case-dependent|Verify vessel, maker, model, urgency and buyer
A6|B&G Alexandria Shipping|Marine agency sourcing need; exact procurement need not public|Sourcing + Commercial Rep|B&G Shipping Agencies|Sourcing fee / commission|Near-term / case-dependent|Qualify live vessel requirement
A7|Alexandria Port Pollution Control|Tender/procurement opportunity; primary terms verify|Tender Readiness + Sourcing|Alexandria Port / buyer|Tender fee + sourcing margin|Deadline-driven|Verify tender scope and OEM
A8|Suez Refinery UPS / Critical Spares|Emergency industrial equipment opportunity; RFQ verify|Emergency Sourcing|Refinery / operator|Sourcing fee / margin|Deadline-driven|Verify RFQ, specs and approved route
A9|Abu Qir Port|Port equipment, marine spares and operational support|Commercial Rep + Sourcing|Abu Qir Port ecosystem|Commission / margin|Near-term|Identify live package and buyer
A10|El Dekheila Terminal|Terminal equipment and marine/industrial spares|Sourcing + Operations Diagnostic|Terminal / port operators|Diagnostic + sourcing margin|Near-term|Map equipment gaps
A11|2026 Egypt O&G Bid Round|New exploration creates future equipment/services demand|Market Entry + OEM Representation|EGPC / EGAS / awarded operators|Retainer + commission|Medium-term|Track awards and map packages
A12|Production Restoration|Well repair/restoration creates intervention demand|Well Services Sourcing|Operators / contractors|Sourcing margin / commission|Near-term|Map projects to equipment packages
A13|Wireline / Slickline Hard-to-Source|Specialized intervention tools may have constrained routes|OEM Representation + Sourcing|Well-service companies / operators|Commission + margin|Near-term|Verify model, territory and alternate OEM
A14|Well Intervention Equipment|Wireline, CT, pressure-control/intervention equipment|OEM Representation + Sourcing|Operators / service companies|Commission / project margin|Near-term|Build OEM shortlist and buyer qualification
A15|Foreign OEM Egypt Entry|Foreign manufacturers need market-entry/channel support|OEM Representation|Foreign OEM ↔ Egypt buyers|Retainer + commission|Near-term|Select OEM, territory, target buyers and agreement
A16|Gulf OEM Representation|Specialized suppliers seek GCC market access|Regional Commercial Rep|Foreign OEM ↔ Gulf buyers|Retainer + commission|Near-term|Verify territory and channel conflict
A17|Land Rig Equipment|Rigs, workover, BOP, mud, pipe handling, spares|OEM Representation + Sourcing|Drilling contractors / operators|Commission + margin|Project-dependent|Identify fleet/maker/model and demand
A18|Offshore Platform Equipment|Offshore drilling/production equipment and critical spares|OEM Representation + Project Support|Offshore operators / contractors|Retainer + commission|Project-dependent|Map asset, OEM and procurement route
A19|Delayed Energy Projects|Delayed projects need recovery, procurement and PMO|Project Recovery + Diagnostic|EPC / energy owners|Diagnostic + PMO fee|Near-term|Screen evidence and quantify delay/cash
A20|Distressed O&G / Energy Companies|Weak profit/cash/productivity may require diagnosis|Turnaround + Financial Diagnostic|O&G / energy companies|Diagnostic + retainer|Case-dependent|Obtain evidence and score distress
A21|Maritime OEM Entry|Marine makers need Egypt/Gulf representation|Commercial Rep|Marine OEM ↔ shipowners / ports|Retainer + commission|Near-term|Choose product, territory and buyers
A22|Shipowner / Manager Emergency Spares|Urgent maker-specific vessel spares|Marine Emergency Sourcing|Shipowners / managers / agents|Sourcing margin|Immediate / case-dependent|Capture vessel, maker, model, port, ETA
A23|Freight Forwarder Operational Diagnostic|Productivity, process, cost and digital gaps|Operational Diagnostic + Digital/AI|Freight forwarders / logistics firms|Diagnostic + implementation|Near-term|Run KPI/process baseline
A24|Shipping Agency Growth|Agencies need commercial development and service expansion|Commercial Development + Rep|Shipping agencies|Retainer + commission|Near-term|Map principals, ports and gaps
A25|Industrial Supplier Market Entry|Specialized suppliers need buyer access and RFQ intelligence|Market Entry + Commercial Rep|Foreign suppliers / OEMs|Retainer + commission|Near-term|Verify territory, certification and buyer fit
A26|ISO 9001:2026 + Executive Training|Readiness/transition and applied management training|ISO Readiness + Training|SMEs / industrial / logistics / energy|Training + diagnostic + implementation|Near-term / recurring|Assessment first; accredited body certifies""")
ws("OPPORTUNITY_MAP",["Priority","Goal","Problem","NAVARIS Service","Counterpart","Revenue Model","Cash Potential","Next Step"],op)
tk=rows("""Business Health Check|Company profile, KPIs, statements|Business model, performance, cash, risk|Executive health score + actions
Financial Diagnostic|P&L, balance sheet, cash flow, debt|Margins, liquidity, leverage, CCC, cash pressure|Financial diagnosis
Operational Diagnostic|Processes, cycle times, output, downtime|Bottlenecks, productivity, capacity, root causes|Improvement plan
Distress Score|Financial/operational/commercial evidence|Profitability, liquidity, debt, cash, trend|Distress score + causes
Project Recovery|Schedule, budget, progress, claims|Critical path, variance, delay causes|Recovery plan + controls
Procurement Diagnostic|Spend, vendors, lead times|Cost, concentration, sourcing gaps|Sourcing strategy
Supply Gap Finder|Requirement, model/spec, territory|Availability, alternatives, route, lead time|Qualified supply shortlist
OEM Representation Scorecard|OEM, product, territory, terms|Fit, access, competition, exclusivity, economics|GO/VERIFY/HOLD decision
Tender Readiness|Tender/RFQ, eligibility, specs|Compliance, capability, gaps, bid economics|Tender readiness pack
Commercial Opportunity Score|Buyer, need, value, timing, access|Fit, urgency, margin, probability, days-to-cash|0–100 priority
Feasibility Engine|Market, CAPEX/OPEX, revenue, financing|NPV, IRR, payback, break-even, DSCR|Business case
Business Simulation|Price, volume, margin, terms, FX|Base/upside/downside/stress|Cash-positive date + decision range
Cash Calculator|Price, cost, commission, payment terms|Expected cash, margin, days-to-cash|Cash-first economics
Supplier Qualification|Company, certifications, references|Technical/commercial/regulatory fit|Qualified supplier/OEM record
Market Entry|OEM/product, geography, buyers|Market signals, routes, competitors, territory|Entry plan + target accounts
ISO 9001:2026 Readiness|QMS docs, processes, risks|Gap assessment, leadership, process/risk controls|Readiness roadmap; certification by accredited body
KPI Management System|Objectives, baseline, targets, owners|Financial/customer/operations/people/digital/commercial KPIs|KPI scorecard
Digital/AI Diagnostic|Systems, workflows, data, pain points|Automation, integration, AI use cases, ROI|Transformation roadmap
Training Diagnostic|Role, sector, skill gaps|Capability gaps linked to KPIs|Applied training plan
Executive Decision Pack|Validated evidence, calculations, options|Trade-offs, scenarios, risk, cash impact|GO/VERIFY/HOLD/NO-GO pack""")
ws("TOOLKIT",["Toolkit","What enters","What analyzes","Client result"],tk)
oi=["NOV|Drilling rigs, intervention, BOP, downhole, automation","Baker Hughes|Wellheads, connectors, casing/liner, subsea/well construction","SLB|Surface equipment, rigs, MPD, wellhead, drilling/production","Halliburton|Completion, well intervention, drilling, pressure control","Weatherford|Drilling, completion, production, intervention, artificial lift","Expro|Well testing, subsea, well intervention, flow management","Hunting|Well completion, OCTG, perforating, downhole systems","Forum Energy Technologies|Drilling, completion, production, subsea, intervention","Drillmec|Onshore/offshore drilling rigs and equipment","WTE Oilfield Solutions|Slickline, braided line, electric line, pressure-test/wireline","Tenaris|OCTG, line pipe, tubular solutions","Vallourec|OCTG, premium connections, tubular solutions","Coretrax|Wellbore remediation, reaming, milling, cleanout tools","Tercel|Drill bits, completion and downhole tools","Leutert|Downhole pressure/temperature and well testing tools","Odfjell Technology|Drilling operations, well services, offshore technology","Archer|Well services, wireline, well integrity, drilling services","EnerMech|Pressure testing, valve/flow control, maintenance services","Arabian Rig Manufacturing (ARM)|Land rigs, rig equipment, offshore drilling packages","GE Vernova|Gas turbines, power equipment, controls, energy systems"]
oif=[]
for x in oi:
    n,p=x.split("|");oif.append([n,p,"OEM direct / authorized channel","VERIFY — Egypt/Gulf territory","VERIFY","VERIFY","VERIFY","VERIFY","VERIFY","VERIFY","VERIFY","VERIFY","TBD","TBD","Primary OEM/product source to verify","Hard-to-Source Candidate — territory verification required"])
ws("OEM_OILFIELD",["Company","Product","Target Route","Egypt/Gulf Presence","Exact Model","Application","Existing Distributor","Exclusivity","Export Route","Lead Time","Buyer","Current Demand","Commission %","Days-to-Cash","Evidence Link","Status / Notes"],oif)
mi=["Wärtsilä|Marine engines, propulsion, automation, electrical","Alfa Laval|Heat exchangers, separators, pumps, marine treatment","Kongsberg Maritime|Navigation, automation, propulsion, deck machinery, DP","MacGregor|Cargo handling, cranes, winches, deck machinery","DESMI|Pumps, ballast, firefighting, oil spill response","Berg Propulsion|Propellers, thrusters, propulsion systems","Jastram|Propulsion, steering gears, control systems","Vulkan|Marine couplings, shaft systems, propulsion components","SKF Marine|Bearings, shaft alignment, condition monitoring, seals","Sperre|Marine compressors and compressed-air systems","Heinen & Hopman|HVAC and climate-control systems","Jowa|Oily-water separators and environmental systems","Evac|Vacuum toilet, wastewater and dry-waste systems","Hoyer Motors|Marine electric motors","Schottel|Marine propulsion and thrusters","Rolls-Royce Solutions / mtu|Marine engines, power systems, automation","ABB Marine & Ports|Electrical systems, drives, automation, shore power","MAN Energy Solutions|Marine engines, turbochargers, propulsion, service","Caterpillar Marine|Marine engines, propulsion and power systems","ZF Marine|Marine transmissions, controls, propellers, propulsion"]
mir=[]
for x in mi:
    n,p=x.split("|");mir.append([n,p,"Emergency spares / OEM representation / sourcing","VERIFY — Egypt/Gulf territory","VERIFY","VERIFY","VERIFY","VERIFY","VERIFY","VERIFY","VERIFY","VERIFY","TBD","TBD","Primary OEM/product source to verify","Hard-to-Source Candidate — territory verification required"])
ws("OEM_MARITIME",["Company","Products","NAVARIS Opportunity","Egypt/Gulf Presence","Exact Model","Application","Existing Distributor","Exclusivity","Export Route","Lead Time","Buyer","Current Demand","Commission %","Days-to-Cash","Evidence Link","Status / Notes"],mir)
m=w["MASTER_3Part_Agreement_First"]; st=m.max_column+2; h=["TOP 3 CASH PRIORITIES","Demand / Opportunity","Supplier / OEM","NAVARIS Role","Revenue Model","Cash Priority","Agreement Status","Evidence / Verification"]
for j,v in enumerate(h,st):m.cell(1,j,v)
top=[["1","A1 EGPC Emergency","INTERSHIP Suez","Emergency Sourcing","Emergency sourcing fee","🥇 Immediate cash","AGREEMENT REQUIRED FIRST","Exact RFQ / part / buyer route must be verified"],["2","A5 Suez Canal emergency","Wärtsilä / Alfa Laval","Marine Emergency Sourcing","Margin","🥉 Very high margin","AGREEMENT REQUIRED FIRST","Vessel/maker/model/buyer/territory must be verified"],["3","A15 Foreign OEM Egypt entry","NOV / Baker Hughes","OEM Representation","Retainer + commission","🥈 Retainer + recurring","AGREEMENT REQUIRED FIRST","Territory/channel/exclusivity/buyer pipeline must be verified"]]
for i,r in enumerate(top,2):
    for j,v in enumerate(r,st):m.cell(i,j,v)
w.save(p)
