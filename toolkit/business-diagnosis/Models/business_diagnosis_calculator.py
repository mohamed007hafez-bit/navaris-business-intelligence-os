def calculate(scores):
    if len(scores)!=7 or any(not isinstance(x,(int,float)) or not 1<=x<=5 for x in scores): raise ValueError("Provide seven scores from 1 to 5")
    return {"dimension_scores":list(scores),"mean_score":sum(scores)/7,"status":"PROPOSED; verify evidence"}
if __name__=="__main__": print(calculate([3]*7))
