import json
manifest={'name':'NAVARIS Private Investment & Intelligence','short_name':'NAVARIS','start_url':'/','display':'standalone','background_color':'#0A192F','theme_color':'#0A192F'}
with open('manifest.json','w') as f: json.dump(manifest,f,indent=2)
sw="self.addEventListener('install',e=>{self.skipWaiting()}); self.addEventListener('fetch',e=>{e.respondWith(fetch(e.request))});"
with open('service-worker.js','w') as f: f.write(sw)
print('PWA built')
