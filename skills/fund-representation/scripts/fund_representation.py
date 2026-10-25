from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[3]/"toolkit"/"fund-representation"/"Models"))
from representation_fees import calculate
def run(inputs): return calculate(**inputs)
if __name__=="__main__": print(run({}))
