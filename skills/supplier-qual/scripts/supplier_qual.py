def calculate(criteria):
    if not isinstance(criteria,dict) or not criteria: raise ValueError("Provide qualification criteria with evidence status")
    missing=sorted(k for k,v in criteria.items() if v is None)
    failed=sorted(k for k,v in criteria.items() if v is False)
    passed=sorted(k for k,v in criteria.items() if v is True)
    return {"passed":passed,"missing":missing,"failed":failed,"decision":"HOLD" if missing or failed else "READY FOR HUMAN REVIEW","status":"PROPOSED; independently verify evidence"}
if __name__=="__main__": print(calculate({"capacity":True,"quality_cert":None}))
