# Works for NAVARIS only - Single Company - Alexandria
"""Agent 08: Subcontractor coordination; no authority to create companies.
Subordinate to Dr. Mohamed Hafez Khalifa, the single NAVARIS master.
Cannot assign tasks, change master policy, or delegate directly to other agents.
"""
AGENT_ID="08"
AGENT_NAME="subcontractor_coordination"
SCOPE="Subcontractor coordination; no authority to create companies"
def execute(task):
    if not isinstance(task,str) or not task.strip(): raise ValueError("A non-empty task is required")
    return {"company":"NAVARIS","base":"Alexandria, Egypt","agent_id":AGENT_ID,"agent_name":AGENT_NAME,"status":"accepted_for_execution","task":task.strip(),"scope":SCOPE,"requires_master_review":True}
