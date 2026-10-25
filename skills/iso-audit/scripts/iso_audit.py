from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[3]/"toolkit"/"iso-audit"/"Models"))
from audit_readiness import calculate
def run(required,evidenced): return calculate(required,evidenced)
if __name__=="__main__": print(run(["scope"],[]))
