def calculate(retainer_monthly=0,months=1,transaction_base=0,success_rate=0,commission_base=0,share_rate=.7):
    vals=(retainer_monthly,months,transaction_base,success_rate,commission_base,share_rate)
    if any(not isinstance(x,(int,float)) or x<0 for x in vals) or not 0<=success_rate<=1 or not 0<=share_rate<=1: raise ValueError("Invalid fee assumptions")
    return {"retainer_total":retainer_monthly*months,"success_fee_scenario":transaction_base*success_rate,"shared_commission_scenario":commission_base*share_rate,"status":"PROPOSED; signed mandate required"}
