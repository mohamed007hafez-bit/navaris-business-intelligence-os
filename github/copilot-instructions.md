"""
Module: navaris_dce_v4_engine
Description: Production-ready core skill for NAVARIS Deal-to-Cash Engine v4.0.
Implements strict zero-capital gating, validation boundaries, and a 7-stage evidence verification protocol.
"""

import json

class NavarisEngineV4:
    def __init__(self, raw_lead_data):
        self.lead = raw_lead_data
        self.state = "PENDING_VERIFICATION"
        self.verification_gates = {
            "SOURCE_VERIFIED": False,
            "BUYER_DEMAND_VERIFIED": False,
            "SUPPLIER_CAPACITY_VERIFIED": False,
            "ZERO_CAPITAL_VERIFIED": False,
            "COMMISSION_TERMS_SIGNED": False,
            "COMPLIANCE_CHECKED": False,
            "FINANCIAL_INPUTS_VALIDATED": False
        }

    def validate_and_bound_inputs(self) -> bool:
        """
        Validates boundaries and forces limits on f_cur (Hard Currency) and a_aci (Customs Distress).
        Prevents division by zero or errors during missing asset data.
        """
        f_cur = self.lead.get("f_cur", 0)
        a_aci = self.lead.get("a_aci", 0)
        
        # Enforce boundaries between 0 and 10
        self.lead["f_cur"] = max(0, min(10, f_cur))
        self.lead["a_aci"] = max(0, min(10, a_aci))
        
        # Validate financial metrics exist to prevent incorrect defaults
        required_financials = ["assets", "liabilities", "nopat", "invested_cap"]
        if not all(k in self.lead for k in required_financials):
            return False
        return True

    def calculate_turnaround_ratios(self) -> dict:
        """
        Calculates financial ratios with strict division protection.
        """
        liabilities = self.lead.get("liabilities", 0)
        assets = self.lead.get("assets", 0)
        nopat = self.lead.get("nopat", 0)
        invested_cap = self.lead.get("invested_cap", 0)

        # Handling mathematical constraints safely
        current_ratio = round(assets / liabilities, 2) if liabilities > 0 else None
        roic = round(nopat / invested_cap, 4) if invested_cap > 0 else 0.0
        
        return {"current_ratio": current_ratio, "roic": roic}

    def run_gating_workflow(self) -> dict:
        """
        Executes the 7-gate verification pipeline before qualifying any asset-light deal.
        """
        if not self.validate_and_bound_inputs():
            self.state = "PENDING_VERIFICATION"
            return {"status": self.state, "reason": "FINANCIAL_INPUTS_VALIDATED Failed. Missing or malformed data."}

        # Calculate classifications
        v_hc = (self.lead["f_cur"] * 6) + (self.lead["a_aci"] * 4)
        ratios = self.calculate_turnaround_ratios()

        # Operational Gate Assertions (Strict Zero-Capital Verification)
        has_source_link = bool(self.lead.get("source_link"))
        has_vetted_suppliers = len(self.lead.get("suppliers", [])) >= 2
        requires_navaris_capital = self.lead.get("requires_upfront_capital", True) # Must be False

        # Evaluate Gates
        if has_source_link: self.verification_gates["SOURCE_VERIFIED"] = True
        if self.lead.get("buyer_confirmed"): self.verification_gates["BUYER_DEMAND_VERIFIED"] = True
        if has_vetted_suppliers: self.verification_gates["SUPPLIER_CAPACITY_VERIFIED"] = True
        if not requires_navaris_capital: self.verification_gates["ZERO_CAPITAL_VERIFIED"] = True
        if self.lead.get("ncnda_signed"): self.verification_gates["COMMISSION_TERMS_SIGNED"] = True
        if self.lead.get("iso_compliant"): self.verification_gates["COMPLIANCE_CHECKED"] = True
        if ratios["current_ratio"] is not None: self.verification_gates["FINANCIAL_INPUTS_VALIDATED"] = True

        # Check if all gates passed
        if all(self.verification_gates.values()) and v_hc >= 75:
            self.state = "QUALIFIED_STRUCTURED_DEAL"
        else:
            self.state = "PENDING_VERIFICATION"

        return {
            "status": self.state,
            "v_hc_score": v_hc,
            "ratios": ratios,
            "gates_log": self.verification_gates
        }
