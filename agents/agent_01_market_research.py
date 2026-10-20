# Works for NAVARIS only - Single Company - Alexandria
"""Agent 01: Egypt-only market research and source verification."""
AGENT_ID="01"
SCOPE="Egypt-only market research and source verification"
def execute(task):
    if not isinstance(task,str) or not task.strip(): raise ValueError("A non-empty task is required")
    return {"company":"NAVARIS","base":"Alexandria, Egypt","agent_id":AGENT_ID,"status":"accepted_for_execution","task":task.strip(),"scope":SCOPE,"requires_master_review":True}
