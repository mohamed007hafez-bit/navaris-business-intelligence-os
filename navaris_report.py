#!/usr/bin/env python3
"""NAVARIS petroleum tender monitor: stdlib-only MVP; human review required."""
import argparse, email.message, hashlib, json, os, sys, smtplib
from datetime import datetime, timezone
from html.parser import HTMLParser
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import urljoin, urlparse
from urllib.request import Request, urlopen
SOURCES = {'GASCO':'https://www.gasco.com.eg/','ENPPI':'https://www.enppi.com/'}
KEYWORDS = ('tender','tenders','procurement','bid','bidding','مناقصة','مناقصات','طرح','مشتريات','ممارسة')
STATE_PATH=Path(os.getenv('NAVARIS_STATE_PATH','data/seen_tenders.json'))
REPORT_PATH=Path(os.getenv('NAVARIS_REPORT_PATH','navaris_daily_report.md'))
def utc_now(): return datetime.now(timezone.utc).replace(microsecond=0).isoformat()
def contains_keyword(value): return any(k.casefold() in (value or '').casefold() for k in KEYWORDS)
def stable_id(company,url,title): return hashlib.sha256(f"{company}|{url.split('#',1)[0].rstrip('/')}|{title.casefold()}".encode()).hexdigest()
class LinkParser(HTMLParser):
 def __init__(self): super().__init__(convert_charrefs=True); self.links=[]; self.href=None; self.parts=[]
 def handle_starttag(self,tag,attrs):
  if tag.lower()=='a': self.href=dict(attrs).get('href'); self.parts=[]
 def handle_data(self,data):
  if self.href is not None: self.parts.append(data)
 def handle_endtag(self,tag):
  if tag.lower()=='a' and self.href is not None: self.links.append((self.href,' '.join(' '.join(self.parts).split()))); self.href=None; self.parts=[]
def fetch_source(company,source_url):
 try:
  req=Request(source_url,headers={'User-Agent':'NAVARIS-TenderMonitor/1.0','Accept':'text/html'})
  with urlopen(req,timeout=20) as response:
   raw=response.read(2_000_001)[:2_000_000]; ctype=response.headers.get('Content-Type','')
   if 'html' not in ctype.lower() and not raw.lstrip().lower().startswith((b'<!doctype html',b'<html')): raise ValueError('Response is not recognized as HTML')
   html=raw.decode(response.headers.get_content_charset() or 'utf-8',errors='replace'); parser=LinkParser(); parser.feed(html); items=[]
   for href,title in parser.links:
    if href and title and contains_keyword(title+' '+href):
     link=urljoin(source_url,href)
     if urlparse(link).scheme in ('http','https'):
      items.append({'company':company,'title':title[:300],'url':link,'source_page':source_url,'id':stable_id(company,link,title),'publication_date':None,'deadline':None,'verification':'Public link candidate; verify tender document manually'})
   unique={x['id']:x for x in items}
   return {'company':company,'source':source_url,'status':'ok','checked_at':utc_now(),'items':list(unique.values())}
 except (HTTPError,URLError,TimeoutError,OSError,ValueError) as exc: return {'company':company,'source':source_url,'status':'source_error','checked_at':utc_now(),'error':f'{type(exc).__name__}: {exc}','items':[]}
def load_seen(path):
 try: return set(json.loads(path.read_text(encoding='utf-8')).get('seen_ids',[]))
 except (FileNotFoundError,json.JSONDecodeError,OSError): return set()
def save_seen(path,ids):
 path.parent.mkdir(parents=True,exist_ok=True); path.write_text(json.dumps({'updated_at':utc_now(),'seen_ids':sorted(ids)},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def build_report(results,new_items,checked_at):
 esc=lambda s:(s or '').replace('|','\\|').replace('\n',' ')
 lines=['# NAVARIS — تقرير المناقصات البترولية اليومي','',f'- وقت الفحص (UTC): {checked_at}','- المصادر: GASCO وENPPI','- الرصد يفحص روابط HTML العامة التي تطابق كلمات مفتاحية فقط.','- **تنبيه:** كل نتيجة مرشح أولي وليست مناقصة مؤكدة حتى مراجعة المستند الرسمي.','','## الفرص الجديدة المرشحة','','| الشركة | المناقصة / الاحتياج الظاهر | تاريخ النشر | آخر موعد | رابط المصدر |','|---|---|---|---|---|']
 if new_items:
  for x in new_items: lines.append(f"| {esc(x['company'])} | {esc(x['title'])} | غير متاح | غير متاح | [فتح المصدر]({x['url']}) |")
 else: lines.append('| — | لا توجد روابط جديدة مطابقة في الصفحات التي أمكن فحصها؛ لا يثبت ذلك عدم وجود مناقصات. | غير متاح | غير متاح | — |')
 lines += ['', '## حالة المصادر','']
 for r in results: lines.append(f"- **{r['company']}**: {'تم الوصول؛ روابط مرشحة: '+str(len(r['items'])) if r['status']=='ok' else 'تعذر التحقق: '+esc(r.get('error',r['status']))}. {r['source']}")
 lines += ['', '## بوابة التقييم الفني والمالي','', 'لا تُحسب درجة رقمية دون كراسة الشروط، بيانات المورد، وأوزان موثقة.','', '1. مطابقة إلزامية: النطاق والمواصفات والتأهيل والضمانات والمواعيد.','2. الدرجة الفنية: مجموع (وزن المعيار × درجته) باستخدام الأوزان المنشورة في المناقصة فقط.','3. التكلفة الكلية = التوريد + الشحن + التأمين + الجمارك/الضرائب + الفحص + التمويل + احتياطي مخاطر موثق.','4. هامش المساهمة = الإيراد الصافي المتحقق منه − التكاليف المتغيرة المباشرة.','5. قرار مبدئي: متابعة / طلب مستندات / استبعاد؛ القرار النهائي بمراجعة بشرية وموافقة الماستر.','', '## حدود التشغيل','- لا يتجاوز السكريبت CAPTCHA أو بوابات تسجيل الدخول ولا يعالج الصفحات المعتمدة على JavaScript أو ملفات PDF.','- تواريخ النشر والإغلاق لا تُخمن.','- هذا MVP لا يثبت أنه أقوى من ChatGPT أو Claude؛ تُقاس الجودة باختبارات موثقة.','']
 return '\n'.join(lines)
def send_email(subject,body):
 keys=['MAIL_SERVER','MAIL_PORT','MAIL_USERNAME','MAIL_PASSWORD','MAIL_FROM','REPORT_EMAIL']
 missing=[k for k in keys if not os.getenv(k)]
 if missing:
  print('EMAIL_SKIPPED: missing optional mail configuration: '+', '.join(missing),file=sys.stderr)
  return False
 msg=email.message.EmailMessage(); msg['Subject']=subject; msg['From']=os.environ['MAIL_FROM']; msg['To']=os.environ['REPORT_EMAIL']; msg.set_content(body)
 with smtplib.SMTP(os.environ['MAIL_SERVER'],int(os.environ['MAIL_PORT']),timeout=25) as smtp: smtp.starttls(); smtp.login(os.environ['MAIL_USERNAME'],os.environ['MAIL_PASSWORD']); smtp.send_message(msg)
 return True
def main():
 import argparse
 ap=argparse.ArgumentParser(); ap.add_argument('--send-failure-alert',action='store_true'); args=ap.parse_args()
 if args.send_failure_alert:
  send_email('[NAVARIS ALERT] فشل تشغيل تقرير المناقصات','تعذر إكمال تشغيل NAVARIS. راجع سجلات GitHub Actions.\n'+os.getenv('NAVARIS_FAILURE_DETAIL','')); return 0
 checked=utc_now(); results=[fetch_source(c,u) for c,u in SOURCES.items()]; seen=load_seen(STATE_PATH); candidates=[x for r in results for x in r['items']]; fresh=[x for x in candidates if x['id'] not in seen]
 report=build_report(results,fresh,checked); REPORT_PATH.parent.mkdir(parents=True,exist_ok=True); REPORT_PATH.write_text(report,encoding='utf-8'); save_seen(STATE_PATH,seen|{x['id'] for x in candidates}); print(report)
 if all(r['status']!='ok' for r in results): print('ERROR: all sources failed',file=sys.stderr); return 2
 try:
  sent=send_email('[NAVARIS] تقرير المناقصات البترولية اليومي',report)
 except Exception as exc: print(f'EMAIL_ERROR: {type(exc).__name__}: {exc}',file=sys.stderr); return 3
 if not sent: print('REPORT_READY: report artifact is available; email delivery is not configured.',file=sys.stderr)
 return 0
if __name__=='__main__': raise SystemExit(main())