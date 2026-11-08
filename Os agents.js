// NAVARIS Autonomous Agents Engine
// FETCH → STORE → ANALYZE → DEVELOP → DECIDE → DELIVER
let payType='Monthly', cur='Business Model', TRUST=0, CASH=0;
const Agents = {
  fetch(q){ log(`⬇ FETCH Agent: Fetching ${q} from Library + Market...`); return q; },
  store(data){ log(`🗄 STORE Agent: Storing in Vault — ${data}`); },
  analyze(){ log(`🔍 ANALYZE Agent: Analyzing vs Library...`); },
  develop(){ log(`⚙ DEVELOP Agent: Developing Model v2...`); },
  decide(score){ log(`🎯 DECIDE Agent: Score ${score} → ${score>=70?'GREEN INVEST':score>=40?'YELLOW Ask More':'RED STOP'}`); },
  deliver(){ log(`🚀 DELIVER Agent: Delivering Report — Dashboard — Green Chart`); }
};
function log(m){ let el=document.getElementById('agentsLog'); if(el) el.innerHTML+=m+'<br>'; console.log(m); }
function pick(el,t){cur=t;document.querySelectorAll('#tasks button').forEach(b=>b.classList.remove('active'));el.classList.add('active');calc();}
function setPay(el,t){payType=t;document.querySelectorAll('.pay button').forEach(b=>b.classList.remove('active'));el.classList.add('active');calc();}
function addType(){let v=document.getElementById('newType').value;if(!v)return;let s=document.getElementById('type');let o=document.createElement('option');o.text=v;s.add(o);s.value=v;document.getElementById('newType').value='';Agents.fetch(v);Agents.store(v);calc();}
function addField(){let d=document.createElement('div');d.className='row';d.innerHTML='<input placeholder="New Field"><button onclick="this.parentElement.remove()">✕</button>';document.getElementById('dyn').appendChild(d);}
function addInv(){let v=document.getElementById('newInv').value;if(!v)return;let s=document.createElement('span');s.className='chip';s.innerText='✕ '+v;s.onclick=function(){this.remove();calc()};document.getElementById('invChips').appendChild(s);document.getElementById('newInv').value='';calc();}
function addEval(){let v=document.getElementById('newEval').value;if(!v)return;let d=document.createElement('div');d.className='row';d.innerHTML='<span>'+v+'</span><input type="range" min="0" max="100" value="50" oninput="calc()"><button onclick="this.parentElement.remove();calc()">✕</button>';document.getElementById('evals').appendChild(d);document.getElementById('newEval').value='';}
function sync1(){let eq=+document.getElementById('eq').value;document.getElementById('eqVal').innerText=eq+'%';document.getElementById('debt').value=100-eq;document.getElementById('debtVal').innerText=(100-eq)+'%';calc();}
function sync2(){let d=+document.getElementById('debt').value;document.getElementById('debtVal').innerText=d+'%';document.getElementById('eq').value=100-d;document.getElementById('eqVal').innerText=(100-d)+'%';calc();}
function addBook(){let v=document.getElementById('newBook').value;if(!v)return;Agents.fetch(v);Agents.store(v);Agents.analyze();Agents.develop();alert('UPGRADE: '+v+' — FETCH → STORE → ANALYZE → DEVELOP → ADDITION — Added to Library');document.getElementById('newBook').value='';}
function updPrice(){let p=document.getElementById('price');if(p)p.innerText='$'+document.getElementById('pack').value;}
function pay(m){CASH=1;TRUST=1;let amt=document.getElementById('pack').value;document.getElementById('payStatus').innerHTML='✅ Payment Success via '+m+' — $'+amt+'<br><b>CASH=1 • TRUST=1 • Score Active</b><br>DELIVER Agent: بيسلم التقرير دلوقتي';Agents.fetch('Payment '+m);Agents.store('Payment '+amt);Agents.deliver();calc();alert('Payment via '+m+' — $'+amt+' — Success! CASH=1 TRUST=1');}
function calc(){
  let cap=+document.getElementById('cap')?.value||100000; let rev=+document.getElementById('rev')?.value||0; let opex=+document.getElementById('opex')?.value||0;
  let eq=+document.getElementById('eq')?.value||30; let amt=+document.getElementById('payAmt')?.value||0;
  let oer=rev?(opex/rev).toFixed(2):0; let profit=rev-opex; let roi=(profit/cap*100).toFixed(1);
  let n=document.querySelectorAll('#evals .row').length; let raw=Math.round(55+(roi>0?roi*0.8:0)+eq*0.2+n*3);
  let score=TRUST===1?raw:raw; // TRUST=0 → Score shown as 0 in decision, but keep raw for debug
  let displayScore = TRUST===1? score : (CASH===0? 0 : score);
  // For demo: if not paid, show raw but note TRUST. Real OS: TRUST=0 → Score=0
  let dec=displayScore>=70?'GREEN - INVEST':displayScore>=40?'YELLOW - Ask More - أعد الحسابات':'RED - STOP';
  let el=document.getElementById('score'); if(el)el.innerText=displayScore;
  let o=document.getElementById('oer'); if(o)o.innerText=oer;
  let r=document.getElementById('roi'); if(r)r.innerText=roi+'%';
  let d=document.getElementById('dec'); if(d){d.innerText=dec; d.style.color=displayScore>=70?'#16A34A':'#D97706';}
  let t=document.getElementById('total'); if(t){let mult=payType=='Monthly'?12:payType=='Quarterly'?4:1; t.innerText='$'+(amt*mult*12).toLocaleString();}
  let ev=document.getElementById('eval'); if(ev) ev.innerHTML='<b>'+cur+' | '+document.getElementById('sector')?.value+' | '+document.getElementById('type')?.value+'</b><br>Capital: $'+cap.toLocaleString()+' | Opinion: '+document.getElementById('opinion')?.value+'<br>Payment: '+payType+' $'+amt.toLocaleString()+' • Fund: '+document.getElementById('fund')?.value+'<br>Ratios: Equity '+eq+'% / Debt '+(100-eq)+'% • OER: '+oer+' • ROI: '+roi+'% • Score: '+displayScore+' • '+dec+' • TRUST: '+TRUST;
  let out=document.getElementById('out'); if(out) out.innerHTML='Score: '+displayScore+' | OER: '+oer+' | ROI: '+roi+'% | Decision: '+dec;
  let capOut=document.getElementById('capOut'); if(capOut) capOut.innerHTML='Invested Capital: $'+cap.toLocaleString()+' | Opinion: '+document.getElementById('opinion')?.value;
}
if(document.getElementById('cap')) calc();
