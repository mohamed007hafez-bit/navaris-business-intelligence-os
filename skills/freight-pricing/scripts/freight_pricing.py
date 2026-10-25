from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[3]/"toolkit"/"freight-forwarding"/"Models"))
from landed_cost import calculate
def run(inputs): return calculate(**inputs)
if __name__=="__main__": print(run({}))
