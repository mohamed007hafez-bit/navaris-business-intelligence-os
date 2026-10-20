# Works for NAVARIS only - Single Company - Alexandria
"""Agent 03: Technical services and rigless-work planning.
Subordinate to Dr. Mohamed Hafez Khalifa, the single NAVARIS master.
Cannot assign tasks, change master policy, or delegate directly to other agents.
"""
AGENT_ID="03"
AGENT_NAME="technical_services"
SCOPE="Technical services and rigless-work planning"
def execute(task):
    if not isinstance(task,str) or not task.strip(): raise ValueError("A non-empty task is required")
    return {"company":"NAVARIS","base":"Alexandria, Egypt","agent_id":AGENT_ID,"agent_name":AGENT_NAME,"status":"accepted_for_execution","task":task.strip(),"scope":SCOPE,"requires_master_review":True}
