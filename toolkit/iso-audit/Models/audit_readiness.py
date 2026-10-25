def calculate(required_items,evidenced_items):
    required=set(required_items); evidenced=set(evidenced_items)
    if not required: raise ValueError("Required items cannot be empty")
    missing=sorted(required-evidenced)
    return {"coverage":len(required & evidenced)/len(required),"missing":missing,"status":"PROPOSED; auditor judgement required"}
