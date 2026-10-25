def calculate(fob,freight,insurance,origin_destination=0,duties_taxes=0,other_fees=0,margin_rate=0):
    costs=(fob,freight,insurance,origin_destination,duties_taxes,other_fees)
    if any(not isinstance(x,(int,float)) or x<0 for x in costs) or margin_rate<0: raise ValueError("Costs and margin must be non-negative")
    total=sum(costs)
    return {"landed_cost":total,"scenario_sell_price":total*(1+margin_rate),"status":"TESTED CALCULATION; verify live quote inputs"}
