def calculate(opening_cash,receipts,payments):
    vals=[opening_cash,*receipts,*payments]
    if any(not isinstance(x,(int,float)) for x in vals): raise TypeError("Numeric cash inputs required")
    return {"closing_cash":opening_cash+sum(receipts)-sum(payments),"status":"PROPOSED; reconcile to bank"}
