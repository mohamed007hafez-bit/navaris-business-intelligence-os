"""Local NAVARIS API, bound to loopback by default."""
import hmac, os
from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel, Field
from core.master import MASTER_KEY, assign_task, health, report_to_master
app=FastAPI(title="NAVARIS - Single Company - Alexandria",version="4.1.0")
class TaskRequest(BaseModel):
    agent_id:str=Field(pattern=r"^(0[1-9]|1[0-3])$")
    task:str=Field(min_length=1,max_length=4000)
class ReportRequest(BaseModel):
    agent_id:str=Field(pattern=r"^(0[1-9]|1[0-3])$")
    status:str=Field(min_length=1,max_length=40)
    detail:str=Field(default="",max_length=2000)
def authorize(key):
    if not key or not hmac.compare_digest(key,MASTER_KEY): raise HTTPException(status_code=403,detail="Master authorization required")
@app.get("/health")
def get_health(): return health()
@app.post("/tasks")
def create_task(payload:TaskRequest,x_navaris_master_key:str|None=Header(default=None)):
    authorize(x_navaris_master_key)
    try: return assign_task(payload.agent_id,payload.task,MASTER_KEY)
    except ValueError as exc: raise HTTPException(status_code=400,detail=str(exc)) from exc
@app.post("/reports")
def agent_report(payload:ReportRequest):
    try: return report_to_master(payload.agent_id,payload.status,payload.detail)
    except ValueError as exc: raise HTTPException(status_code=400,detail=str(exc)) from exc
if __name__=="__main__":
    import uvicorn
    uvicorn.run(app,host=os.environ.get("NAVARIS_HOST","127.0.0.1"),port=8000)
