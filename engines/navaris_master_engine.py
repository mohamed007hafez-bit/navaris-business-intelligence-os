# engines/navaris_master_engine.py
# NAVARIS Business Intelligence OS — v20 Master Core Engine
# Operating Philosophy: TARGET → CASH 1ST → FLOW | Primary KPI: CASH COLLECTED

class NavarisMasterCoreEngine:
    def __init__(self):
        self.system_charter = "NAVARIS v20 Master Specification"
        # العائلات السلعية والمعدات المتخصصة غير القابلة للتصنيع محلياً (EPC)
        self.specialized_assets = ['API 610 Pumps', 'Wellhead Systems', 'BOP Stacks', 'LPG Hoses']
        # شبكات العلاقات والصناديق الإستراتيجية لتمرير الصفقات
        self.strategic_networks = ['Family Business', 'Private Equity', 'Asset Management', 'McKinsey', 'BCG']

    def calculate_master_cash_equation(self, cash_received: float, refunds: float, direct_costs: float) -> dict:
        """
        تطبيق معادلة الكاش الماستر للنظام (INV-01):
        Formula 1: Collected Cash = Cash Received - Cash Refunds
        Formula 2: Net Contribution = Collected Cash - Direct Delivery Costs
        """
        collected_cash = cash_received - refunds
        net_contribution = collected_cash - direct_costs
        return {
            "collected_cash": collected_cash,
            "net_contribution": net_contribution
        }

    def evaluate_distressed_company(self, company_name: str, metrics: dict) -> dict:
        """
        المسار الأول: فحص وتحليل الشركات المتعثرة معلنة القوائم المالية
        كشف عيوب التشغيل والتكاليف لبناء عروض الاستشارات والتدريب المعرفي
        """
        revenue = metrics.get("revenue", 0.0)
        opex = metrics.get("operating_expenses", 0.0)
        current_assets = metrics.get("current_assets", 0.0)
        current_liabilities = metrics.get("current_liabilities", 0.0)

        current_ratio = current_assets / current_liabilities if current_liabilities > 0 else 0.0
        operating_margin = ((revenue - opex) / revenue) * 100 if revenue > 0 else 0.0

        status = "HEALTHY"
        action = "Monitor operational boundaries."

        if current_ratio < 1.2 or metrics.get("net_income", 0) < 0:
            status = "FINANCIAL_DISTRESS"
            action = "Link with Private Equity networks for asset restructuring and debt optimization."
        elif operating_margin < 10.0:
            status = "OPERATIONAL_DISTRESS"
            action = "Deploy NAVARIS Cost-Optimization Workshops and Corporate Management restructuring models."

        return {
            "company": company_name,
            "current_ratio": round(current_ratio, 2),
            "operating_margin": f"{round(operating_margin, 2)}%",
            "diagnosis": status,
            "recommended_consulting_action": action
        }

    def evaluate_stalled_project_integration(self, project_name: str, missing_component: str, suppliers_list: list) -> dict:
        """
        المسار الثاني: إنقاذ المشاريع المتأخرة والربط بالموردين الكبار والمصانع
        """
        if missing_component not in self.specialized_assets:
            return {"status": "HOLD", "reason": f"Component '{missing_component}' is outside NAVARIS EPC focus."}
            
        qualified_suppliers = [s for s in suppliers_list if s.get("capability") == missing_component]
        
        if not qualified_suppliers:
            return {"status": "HOLD", "reason": "No qualified heavy factory found in registry for this component."}

        return {
            "status": "GO",
            "project": project_name,
            "action": f"Integrate {qualified_suppliers[0]['name']} to resolve supply bottleneck as Third-Party Broker.",
            "commission_potential": "Secure transactional commission from factory supply value."
        }

    def scan_international_tender(self, tender_data: dict) -> dict:
        """
        المسار الثالث: المناقصات الحكومية والدولية (مثل US Tenders)
        تحديد صيغة الدخول الرسمية كطرف ثانٍ أو ثالث (Subcontractor) بناءً على الموقع الإستراتيجي
        """
        required_asset = tender_data.get("required_asset")
        tender_id = tender_data.get("tender_id")

        if required_asset not in self.specialized_assets:
            return {"status": "KILL", "reason": "Tender requirement does not match specialized EPC asset family."}

        return {
            "status": "GO",
            "tender_id": tender_id,
            "legal_position": "Subcontractor (Third-Party Service Provider / Commercial Representative)",
            "execution_path": "Leverage Tier-1 consulting or Asset Management partner networks to fulfill financial backing criteria."
        }

if __name__ == "__main__":
    # فحص تشغيلي متكامل لجميع وظائف الماستر كورد في نظام NAVARIS
    engine = NavarisMasterCoreEngine()
    
    # 1. اختبار معادلة الكاش
    cash_flow = engine.calculate_master_cash_equation(cash_received=500000, refunds=0, direct_costs=45000)
    print(f"[*] Master Cash Collected: {cash_flow['collected_cash']} EGP")
    
    # 2. اختبار فحص الشركات المتعثرة
    company_check = engine.evaluate_distressed_company("Alexandria Logistics Corp", {
        "revenue": 5000000, "operating_expenses": 4800000, "net_income": -100000, "current_assets": 1500000, "current_liabilities": 1800000
    })
    print(f"[*] Corporate Diagnosis: {company_check['diagnosis']} -> Action: {company_check['recommended_consulting_action']}")
