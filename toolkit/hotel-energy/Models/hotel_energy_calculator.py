"""Corporate room-rate scenario; not a live hotel quote."""
def corporate_rate(bar=2000, discount=0.2, factor=0.85):
    if any(not isinstance(v, (int, float)) for v in (bar, discount, factor)):
        raise TypeError("BAR, discount and factor must be numeric")
    if bar < 0 or not 0 <= discount <= 1 or factor < 0:
        raise ValueError("Invalid rate assumptions")
    return bar * (1 - discount) * factor

def commission(bar, corp):
    if any(not isinstance(v, (int, float)) or v < 0 for v in (bar, corp)):
        raise ValueError("BAR and corporate rate must be non-negative numbers")
    return (bar - corp) + bar * 0.10

if __name__ == "__main__":
    bar = 2000
    corp = corporate_rate(bar)
    print({"bar_egp": bar, "scenario_corporate_rate_egp": corp,
           "scenario_commission_egp": commission(bar, corp),
           "status": "SCENARIO ONLY; confirm property rate and commercial terms directly"})
