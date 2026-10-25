from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[3]/"toolkit"/"financial-diagnosis"/"Models"))
from Z_Score_Calculator import calculate
def run(inputs): return calculate(*(inputs[k] for k in ("x1","x2","x3","x4","x5")))
if __name__=="__main__": print(run(dict(x1=.2,x2=.1,x3=.08,x4=1.5,x5=1.2)))
