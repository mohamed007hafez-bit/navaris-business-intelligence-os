"""Scenario calculator; values are assumptions, not market-verified fees."""
def calculate_retainer(base=2000, success_pct=0.03, deal_value=1000000):
    if not isinstance(base,(int,float)) or not isinstance(deal_value,(int,float)) or not isinstance(success_pct,(int,float)):
        raise TypeError("base, success_pct and deal_value must be numeric")
    if base < 0 or deal_value < 0 or not 0 <= success_pct <= 1:
        raise ValueError("Use non-negative amounts and success_pct between 0 and 1")
    return base + deal_value * success_pct
if __name__ == "__main__":
    print({"monthly_retainer_plus_success_fee_scenario": calculate_retainer(), "status":"PROPOSED assumptions; not a quote"})
