def calculate(x1,x2,x3,x4,x5):
    xs=(x1,x2,x3,x4,x5)
    if any(not isinstance(x,(int,float)) for x in xs): raise TypeError("Numeric inputs required")
    return {"z_score":1.2*x1+1.4*x2+3.3*x3+0.6*x4+x5,"status":"PROPOSED; validate model domain"}
if __name__=="__main__": print(calculate(.2,.1,.08,1.5,1.2))
