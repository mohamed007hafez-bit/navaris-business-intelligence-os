from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[3]/"toolkit"/"business-diagnosis"/"Models"))
from business_diagnosis_calculator import calculate
def run(scores): return calculate(scores)
if __name__=="__main__": print(run([3]*7))
