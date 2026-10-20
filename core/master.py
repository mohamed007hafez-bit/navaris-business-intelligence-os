"""NAVARIS One Main Master; sole task-assignment authority."""
import argparse, json, sqlite3, time
from pathlib import Path
MASTER_KEY = "NAVARIS-MASTER-2026"
ROOT = Path(__file__).resolve().parents[1]
DB_PATH = ROOT / "data" / "navaris.sqlite3"
AGENT_IDS = tuple(f"{i:02d}" for i in range(1,14))
def _connect():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    c=sqlite3.connect(DB_PATH, timeout=10)
    c.execute("CREATE TABLE IF NOT EXISTS tasks (id INTEGER PRIMARY KEY, agent_id TEXT NOT NULL, task TEXT NOT NULL, status TEXT NOT NULL DEFAULT 'queued', created_at TEXT DEFAULT CURRENT_TIMESTAMP)")
    c.commit()
    return c
def report_to_master(agent_id, status, detail=""):
    if agent_id not in AGENT_IDS: raise ValueError("Unknown NAVARIS agent")
    report={"agent_id":agent_id,"status":str(status)[:40],"detail":str(detail)[:2000],"timestamp":time.strftime("%Y-%m-%dT%H:%M:%SZ",time.gmtime())}
    p=ROOT/"data"/"agent-reports.jsonl"; p.parent.mkdir(parents=True,exist_ok=True)
    with p.open("a",encoding="utf-8") as f: f.write(json.dumps(report,ensure_ascii=False)+"\n")
    return report
def assign_task(agent_id, task, master_key=None):
    if master_key is not None and master_key != MASTER_KEY: raise PermissionError("Invalid master key")
    if agent_id not in AGENT_IDS: raise ValueError("Agent must be 01-13")
    if not isinstance(task,str) or not task.strip(): raise ValueError("Task cannot be empty")
    with _connect() as c:
        cur=c.execute("INSERT INTO tasks(agent_id,task) VALUES(?,?)",(agent_id,task.strip()))
        return {"task_id":cur.lastrowid,"agent_id":agent_id,"status":"queued","task":task.strip()}
def health():
    with _connect() as c: count=c.execute("SELECT COUNT(*) FROM tasks").fetchone()[0]
    return {"service":"NAVARIS","company_count":1,"base":"Alexandria, Egypt","master":"Dr. Mohamed Hafez Khalifa","database":"ok","registered_agents":13,"tasks_total":count,"status":"healthy"}
def main():
    p=argparse.ArgumentParser(); p.add_argument("--health",action="store_true",help="Run health check")
    s=p.add_subparsers(dest="cmd")
    s.add_parser("health"); a=s.add_parser("assign"); a.add_argument("--agent",required=True,choices=AGENT_IDS); a.add_argument("--task",required=True)
    x=p.parse_args()
    if x.health or x.cmd in (None,"health"): print(json.dumps(health(),indent=2)); return 0
    print(json.dumps(assign_task(x.agent,x.task,MASTER_KEY),indent=2)); return 0
if __name__=="__main__": raise SystemExit(main())
