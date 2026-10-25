"""Corporate room-rate scenario; not a live hotel quote."""
def corporate_rate(bar=2000, discount=0.2, longstay=0.85):
    if not isinstance(bar,(int,float)) or not isinstance(discount,(int,float)) or not isinstance(longstay,(int,float)):
        raise TypeError("bar, discount and longstay must be numeric")
    if bar < 0 or not 0 <= discount <= 1 or longstay < 0:
        raise ValueError("Invalid rate assumptions")
    return bar * (1-discount) * longstay
if __name__ == "__main__":
    print({"scenario_rate":corporate_rate(),"status":"PROPOSED; verify property directly"})
