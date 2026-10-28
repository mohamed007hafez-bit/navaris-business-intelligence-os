"""Shipping landed-cost helper. Never invent rates."""
from decimal import Decimal, InvalidOperation
def _decimal(value,field):
 try: n=Decimal(str(value))
 except (InvalidOperation,ValueError,TypeError): raise ValueError(f"{field} must be a valid number") from None
 if not n.is_finite() or n<0: raise ValueError(f"{field} must be finite and non-negative")
 return n
def analyze_shipping(payload):
 payload=payload or {}; required=("freight","customs","handling")
 missing=[k for k in required if payload.get(k) in (None,"")]
 out={"agent":"shipping","status":"needs_inputs" if missing else "calculated","missing_inputs":missing,"currency":str(payload.get("currency","USD")).upper(),"note":"No market rates are assumed; values are user-supplied and require source evidence."}
 if missing: out["total_landed_cost"]=None; return out
 values={k:_decimal(payload[k],k) for k in required}
 if payload.get("insurance") not in (None,""): values["insurance"]=_decimal(payload["insurance"],"insurance")
 total=sum(values.values(),Decimal("0")); out["line_items"]={k:str(v) for k,v in values.items()}; out["total_landed_cost"]=str(total)
 if payload.get("benchmark") not in (None,""):
  benchmark=_decimal(payload["benchmark"],"benchmark"); saving=benchmark-total
  out["benchmark"]=str(benchmark); out["variance_vs_benchmark"]=str(saving)
  out["saving_percent"]=str((saving/benchmark*100).quantize(Decimal("0.01"))) if benchmark else None
 return out
