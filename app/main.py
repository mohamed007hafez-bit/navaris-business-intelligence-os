# app/main.py
# NAVARIS Business Intelligence OS - Main Operations Dashboard
# Primary KPI: CASH COLLECTED | Framework: Terminal Command Interface (CLI)

import sys
# استدعاء المحركات الحتمية التي قمنا ببرمجتها سابقاً في المجلدات الأخرى
# لضمان معالجة البيانات بدقة وبناءً على سلسلة الأدلة
sys.path.append('.') 
try:
    from engines.gate_engine import NavarisGateEngine
    from engines.financial_engine import NavarisFinancialEngine
except ImportError:
    # حماية مرنة للكود في حال التشغيل الأولي المستقل
    NavarisGateEngine = None
    NavarisFinancialEngine = None

class NavarisOSConsole:
    def __init__(self):
        self.system_name = "NAVARIS Business Intelligence OS"
        self.version = "1.0.0"
        
    def display_dashboard(self, active_deals: list):
        print("=" * 60)
        print(f" {self.system_name} - v{self.version} ".center(60, "#"))
        print("=" * 60)
        print(f"[*] Core Objective: MAXIMIZE CASH COLLECTED")
        print(f"[!] Active Pipeline Operations: {len(active_deals)} Transactions")
        print("-" * 60)
        
        total_projected_commission = 0.0
        
        for idx, deal in enumerate(active_deals, 1):
            print(f"\n[Deal #{idx}] Asset: {deal['product_family']} | Client: {deal['client']}")
            print(f"    -> Current Stage: {deal['current_gate']}")
            
            # تشغيل المحرك المالي لحساب الأرقام بشكل حتمي
            if NavarisFinancialEngine:
                fin_engine = NavarisFinancialEngine()
                analysis = fin_engine.calculate_deal_profitability(
                    product_family=deal['product_family'],
                    base_cost=deal['base_cost'],
                    shipping_cost=deal['shipping_cost'],
                    target_quote=deal['target_quote'],
                    commission_rate=deal['commission_rate']
                )
                
                if analysis['status'] == "GO":
                    comm = analysis['metrics']['net_commission']
                    total_projected_commission += comm
                    print(f"    -> Financial Status: APPROVED ✅")
                    print(f"    -> Projected NAVARIS Commission: {comm:,.2f} EGP")
                else:
                    print(f"    -> Financial Status: HOLD/KILL ⚠️ (Reason: {analysis.get('reason', 'Check metrics')})")
            
            # تشغيل محرك البوابات للتحقق من سلامة الأدلة قبل التنفيذ
            if NavarisGateEngine:
                gate_engine = NavarisGateEngine()
                gate_check = gate_engine.verify_evidence_chain(deal, deal['current_gate'])
                if gate_check['status'] != "GO":
                    print(f"    -> Security Alert: STOPPED at {deal['current_gate']} due to missing evidence!")
                    print(f"       [Reason]: {gate_check['reason']}")
                    
        print("\n" + "=" * 60)
        print(f" TOTAL PROJECTED PIPELINE REVENUE: {total_projected_commission:,.2f} EGP ".center(60, "-"))
        print("=" * 60)

if __name__ == "__main__":
    # محاكاة لخط تشغيل العمليات الحالي في قطاع الطاقة والتوريدات
    pipeline_data = [
        {
            "client": "Suez Petroleum",
            "product_family": "API 610 Pumps",
            "base_cost": 2100000.0,
            "shipping_cost": 85000.0,
            "target_quote": 2600000.0,
            "commission_rate": 5.0,
            "current_gate": "G5",
            "fact": "Official inquiry received via broker",
            "source": "Suez RFQ Document #2026-X",
            "requirement": "API 610 standard heavy-duty pumps",
            "priority_asset": "Refinery Complex",
            "supplier_code": "OEM-EU-04",
            "supply_fit_proven": True,
            "human_approved": True
        },
        {
            "client": "Western Desert Drillers",
            "product_family": "BOP",
            "base_cost": 950000.0,
            "shipping_cost": 40000.0,
            "target_quote": 1000000.0, # تسعير خاطئ مستهدف تحت نقطة التعادل
            "commission_rate": 4.0,
            "current_gate": "G5",
            "fact": "Urgent blowout preventer needed",
            "source": "Direct phone log with operations manager",
            "requirement": "13-5/8 5K BOP Stack",
            "priority_asset": "Rig 14",
            "supplier_code": "OEM-US-09",
            "supply_fit_proven": True,
            "human_approved": True
        }
    ]
    
    console = NavarisOSConsole()
    console.display_dashboard(pipeline_data)
