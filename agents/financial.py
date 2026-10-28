"""Basic financial metrics from explicitly supplied figures."""
from decimal import Decimal, InvalidOperation
def _num(value,field):
 try: n=Decimal(str(value))
 except (InvalidOperation,ValueError,TypeError): raise ValueError(f"{field} must be a valid number") from None
 if not n.is_finite(): raise ValueError(f"{field} must be finite")
 return n
def analyze_financial(payload):
 payload=payload or {}; required=("current_assets","current_liabilities","revenue")
 missing=[k for k in required if payload.get(k) in (None,"")]
 out={"agent":"financial","status":"needs_inputs" if missing else "calculated","missing_inputs":missing,"note":"Uses supplied figures only; not an audit or investment recommendation."}
 if missing: return out
 values={k:_num(payload[k],k) for k in required}
 for k in ("ebitda","inventory"):
  if payload.get(k) not in (None,""): values[k]=_num(payload[k],k)
 ca,cl,rev=values["current_assets"],values["current_liabilities"],values["revenue"]
 out["current_ratio"]=str((ca/cl).quantize(Decimal("0.01"))) if cl else None; out["working_capital"]=str(ca-cl)
 if "ebitda" in values: out["ebitda_margin_percent"]=str((values["ebitda"]/rev*100).quantize(Decimal("0.01"))) if rev else None
 if "inventory" in values: out["inventory"]=str(values["inventory"])
 out["currency"]=str(payload.get("currency","USD")).upper()
 return out
