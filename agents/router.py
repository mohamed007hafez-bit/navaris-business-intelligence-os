"""Deterministic router for three NAVARIS core agents."""
import json,sys
from .shipping import analyze_shipping
from .oilfield import qualify_oilfield
from .financial import analyze_financial
from .database import save_run
ROUTES={"shipping":analyze_shipping,"oilfield":qualify_oilfield,"financial":analyze_financial}
def route_request(request,persist=True):
 if not isinstance(request,dict): raise TypeError("request must be a JSON object")
 agent=str(request.get("agent","")).strip().lower()
 if agent not in ROUTES: raise ValueError("agent must be one of: shipping, oilfield, financial")
 payload=request.get("payload",{})
 if not isinstance(payload,dict): raise TypeError("payload must be a JSON object")
 result=ROUTES[agent](payload)
 if persist: save_run(agent,json.dumps(payload,ensure_ascii=False),json.dumps(result,ensure_ascii=False))
 return result
def main():
 try: print(json.dumps(route_request(json.loads(sys.stdin.read() or "{}")),ensure_ascii=False,indent=2))
 except Exception as exc: print(json.dumps({"status":"error","error":str(exc)},ensure_ascii=False)); raise SystemExit(1)
if __name__=="__main__": main()
