import importlib.util
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def load(path,name):
 spec=importlib.util.spec_from_file_location(name,ROOT/path); mod=importlib.util.module_from_spec(spec); spec.loader.exec_module(mod); return mod
def test_fund_representation_formula():
 m=load(Path("toolkit/fund-representation/Models/fund_representation_calculator.py"),"fundcalc")
 assert m.calculate_retainer(2000,.03,1000000)==32000

def test_hotel_rate_formula():
 m=load(Path("toolkit/hotel-energy/Models/hotel_energy_calculator.py"),"hotelcalc")
 assert round(m.corporate_rate(2000,.2,.85),2)==1360

def test_landed_cost_formula():
 m=load(Path("toolkit/freight-forwarding/Models/landed_cost.py"),"freightcalc")
 assert m.calculate(1000,200,20)["landed_cost"]==1220

def test_altman_z_formula():
 m=load(Path("toolkit/financial-diagnosis/Models/Z_Score_Calculator.py"),"zcalc")
 assert round(m.calculate(.2,.1,.08,1.5,1.2)["z_score"],4)==2.744
