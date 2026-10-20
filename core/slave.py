"""Subordinate execution only; agents report to master and cannot assign work."""
from core.master import AGENT_IDS, report_to_master
def execute_task(agent_id, task, executor=None):
    if agent_id not in AGENT_IDS: raise ValueError("Unregistered NAVARIS agent")
    if not isinstance(task,str) or not task.strip(): raise ValueError("Task cannot be empty")
    report_to_master(agent_id,"started",task)
    try:
        result=executor(task) if executor else {"accepted":True,"note":"Task accepted; task-specific executor required for execution."}
        report_to_master(agent_id,"completed",str(result))
        return {"agent_id":agent_id,"status":"completed","result":result}
    except Exception as exc:
        report_to_master(agent_id,"error",str(exc)); raise
