def calculate(bar,discount_rate=0,long_stay_factor=1,taxes_fees=0,commission_rate=0):
    if bar<0 or taxes_fees<0 or not 0<=discount_rate<=1 or long_stay_factor<0 or not 0<=commission_rate<=1: raise ValueError("Invalid input range")
    net=bar*(1-discount_rate)*long_stay_factor
    return {"room_rate":net,"total_rate":net+taxes_fees,"commission_scenario":net*commission_rate,"status":"PROPOSED; not a quote"}
