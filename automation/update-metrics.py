import json, datetime, os
os.makedirs('data', exist_ok=True)
path='data.json'
data={}
if os.path.exists(path):
    try:
        with open(path,'r') as f: data=json.load(f)
    except Exception: pass
data.update({"aum":"$18.4B","performance":"+12.6%","portfolio":47,"routes":22,"last_updated":datetime.datetime.now().isoformat()})
with open(path,'w') as f: json.dump(data,f,indent=2)
print("Metrics updated")
