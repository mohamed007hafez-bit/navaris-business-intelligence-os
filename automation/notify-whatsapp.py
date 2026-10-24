#!/usr/bin/env python3
"""Send WhatsApp via Meta Cloud API when configured; otherwise timestamp-log the message.
Required to send: WHATSAPP_TOKEN, WHATSAPP_PHONE_NUMBER_ID, WHATSAPP_TO.
"""
import json, os, sys
from datetime import datetime, timezone
import requests
LOG_PATH="reports/whatsapp-log.txt"
def log(message):
    os.makedirs(os.path.dirname(LOG_PATH),exist_ok=True)
    with open(LOG_PATH,"a",encoding="utf-8") as f:
        f.write(f"[{datetime.now(timezone.utc).isoformat()}] {message}\n")
def send_whatsapp(message):
    token=os.getenv("WHATSAPP_TOKEN")
    phone_id=os.getenv("WHATSAPP_PHONE_NUMBER_ID")
    recipient=os.getenv("WHATSAPP_TO")
    if not token or not phone_id or not recipient:
        log("NOT SENT (Cloud API not fully configured). Message: "+message.replace("\n"," "))
        print("WhatsApp not sent: set WHATSAPP_TOKEN, WHATSAPP_PHONE_NUMBER_ID, and WHATSAPP_TO. Message logged.")
        return False
    url=f"https://graph.facebook.com/v20.0/{phone_id}/messages"
    payload={"messaging_product":"whatsapp","to":recipient,"type":"text","text":{"preview_url":False,"body":message}}
    try:
        response=requests.post(url,headers={"Authorization":f"Bearer {token}","Content-Type":"application/json"},json=payload,timeout=20)
        if response.ok:
            body=response.json()
            msgid=(body.get("messages") or [{}])[0].get("id","unknown")
            log(f"API ACCEPTED recipient={recipient} message_id={msgid}")
            print(f"WhatsApp Cloud API accepted message; id={msgid}. Delivery status requires webhook/provider confirmation.")
            return True
        log(f"API ERROR status={response.status_code} response={response.text[:1000]}")
        print(f"WhatsApp API failed ({response.status_code}); details logged.")
        return False
    except requests.RequestException as exc:
        log(f"REQUEST ERROR {type(exc).__name__}: {exc}")
        print("WhatsApp request failed; details logged.")
        return False
if __name__=="__main__":
    msg=" ".join(sys.argv[1:]).strip()
    if not msg: raise SystemExit("Usage: python automation/notify-whatsapp.py \"message text\"")
    raise SystemExit(0 if send_whatsapp(msg) else 1)
