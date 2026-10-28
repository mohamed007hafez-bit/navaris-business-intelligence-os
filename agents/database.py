"""Local SQLite placeholder; unencrypted and not for confidential data."""
import sqlite3
from datetime import datetime,timezone
from .config import DATA_DIR,DB_PATH
def connect():
 DATA_DIR.mkdir(parents=True,exist_ok=True); db=sqlite3.connect(str(DB_PATH))
 db.execute("""CREATE TABLE IF NOT EXISTS agent_runs(id INTEGER PRIMARY KEY AUTOINCREMENT,created_at TEXT NOT NULL,agent TEXT NOT NULL,request_json TEXT NOT NULL,result_json TEXT NOT NULL)"""); db.commit(); return db
def save_run(agent,request_json,result_json):
 with connect() as db: db.execute("INSERT INTO agent_runs(created_at,agent,request_json,result_json) VALUES(?,?,?,?)",(datetime.now(timezone.utc).isoformat(),agent,request_json,result_json))
def list_runs(limit=50):
 limit=max(1,min(int(limit),500))
 with connect() as db: rows=db.execute("SELECT id,created_at,agent,request_json,result_json FROM agent_runs ORDER BY id DESC LIMIT ?",(limit,)).fetchall()
 return [{"id":r[0],"created_at":r[1],"agent":r[2],"request":r[3],"result":r[4]} for r in rows]
