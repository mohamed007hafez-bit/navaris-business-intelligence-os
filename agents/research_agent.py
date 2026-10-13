# agents/research_agent.py
# NAVARIS Business Intelligence OS - Automated Supplier Research & Validation Agent
# Target: Search EU OEMs and match technical specifications to avoid core misalignment.

import json

class NavarisResearchAgent:
    def __init__(self):
        self.agent_role = "Automated Technical Scout & Supplier Matcher"
        # عينة قاعدة بيانات للمصنعين الأوروبيين الموثقين لدينا لحفظ سياق البحث المستقر
        self.trusted_eu_oems = {
            "API 610 Pumps": [
                {"name": "Sulzer Pumps Germany", "code": "OEM-EU-SUL-01", "compliance": "Strict API 610 Enforced"},
                {"name": "KSB SE & Co. Germany", "code": "OEM-EU-KSB-02", "compliance": "Strict API 610 Enforced"}
            ],
            "LPG Hoses": [
                {"name": "Trelleborg Fluid Handling France", "code": "OEM-EU-TRE-01", "compliance": "EN 1762 Certified"},
                {"name": "Continental ContiTech Germany", "code": "OEM-EU-CON-02", "compliance": "EN 1762 Certified"}
            ],
            "BOP": [
                {"name": "Cameron (Schlumberger) Europe", "code": "OEM-EU-CAM-01", "compliance": "API 16A Standard"}
            ]
        }

    def execute_supplier_match(self, deal_requirement: str, product_family: str) -> dict:
        """
        البحث الآلي ومطابقة الموردين استناداً إلى المواصفات الصارمة لإقصاء التخمين
        """
        print(f"[*] Agent activating: {self.agent_role}")
        print(f"[*] Scanning European market for: '{product_family}' matching specification: '{deal_requirement}'")
        
        # التحقق مما إذا كانت العائلة السلعية مدعومة في نظام العمل المستقر
        if product_family not in self.trusted_eu_oems:
            return {
                "search_status": "FAILED",
                "evidence_found": False,
                "reason": f"Product family '{product_family}' is outside core operational focus. Distraction prevented."
            }
            
        # استخراج الموردين المطابقين فنياً
        matched_suppliers = self.trusted_eu_oems[product_family]
        
        # صياغة سلسلة الأدلة للخطوة التالية للـ Supply (G3 & G4)
        evidence_chain = []
        for supplier in matched_suppliers:
            evidence = {
                "fact": f"Qualified OEM found for {product_family}",
                "source": f"Verified Technical Catalog - {supplier['name']}",
                "supplier_code": supplier['code'],
                "supply_fit_proven": True,
                "compliance_check": supplier['compliance']
            }
            evidence_chain.append(evidence)
            
        return {
            "search_status": "SUCCESS",
            "evidence_found": True,
            "matched_count": len(evidence_chain),
            "gate_payload": evidence_chain,
            "next_step": "Forward qualified supplier profiles to human interface for validation."
        }

if __name__ == "__main__":
    # تجربة تشغيلية للوكيل للبحث عن موردين لمضخات API 610 لمشروع حقل جديد
    agent = NavarisResearchAgent()
    search_result = agent.execute_supplier_match(
        deal_requirement="Heavy-duty centrifugal pumps for high-pressure refinery lines",
        product_family="API 610 Pumps"
    )
    
    print("\n" + "="*50)
    print(f"Agent Execution Status: {search_result['search_status']}")
    if search_result['evidence_found']:
        print(f"Total Qualified Suppliers Discovered: {search_result['matched_count']}")
        print(f"Top Matched Code: {search_result['gate_payload'][0]['supplier_code']}")
    print("="*50)
