# navaris_sync_master.py
# NAVARIS Business Intelligence OS - Local Automation Master Push Script
# Target: Automate repository updates directly from mobile without browser errors

import urllib.request
import json
import base64

# ==================== إعدادات الاتصال بالحساب المكتملة ====================
GITHUB_TOKEN = "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"
REPO_OWNER = "mohamed007hafez-bit"
REPO_NAME = "navaris-business-intelligence-os"
# =========================================================================

def push_to_github(file_path, file_content, commit_message):
    """
    يقوم بإنشاء أو تحديث الملفات مباشرة داخل مستودع GitHub بالشكل الصحيح لـ API
    """
    # الرابط البرمجي الرسمي والمصحح للاتصال بـ GitHub API
    url = f"https://github.com{REPO_OWNER}/{REPO_NAME}/contents/{file_path}"
    
    # 1. التحقق من وجود الملف للحصول على الـ SHA (مطلوب للتحديث)
    req = urllib.request.Request(url)
    req.add_header("Authorization", f"token {GITHUB_TOKEN}")
    req.add_header("Accept", "application/vnd.github.v3+json")
    req.add_header("User-Agent", "Navaris-OS-Agent")
    
    sha = None
    try:
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode())
            sha = data['sha']
    except urllib.error.HTTPError as e:
        if e.code != 404: # 404 تعني أن الملف جديد تماماً وسننشئه لأول مرة
            print(f"❌ خطأ فحص {file_path}: {e.read().decode()}")
            return

    # 2. تحويل الكود إلى Base64 (شرط أساسي لـ GitHub API)
    encoded_content = base64.b64encode(file_content.encode('utf-8')).decode('utf-8')
    
    payload = {
        "message": commit_message,
        "content": encoded_content,
        "branch": "main"
    }
    if sha:
        payload["sha"] = sha # تزويد السيرفر بالـ sha إذا كان الملف تحديثاً وليس إنشاءً جديداً

    # 3. إرسال طلب الرفع (PUT Request)
    req_put = urllib.request.Request(url, data=json.dumps(payload).encode('utf-8'), method='PUT')
    req_put.add_header("Authorization", f"token {GITHUB_TOKEN}")
    req_put.add_header("Content-Type", "application/json")
    req_put.add_header("Accept", "application/vnd.github.v3+json")
    req_put.add_header("User-Agent", "Navaris-OS-Agent")
    
    try:
        with urllib.request.urlopen(req_put) as response:
            if response.status in:
                print(f"▲ تم رفع وتحديث بنجاح: {file_path} 🚀")
            else:
                print(f"⚠️ استجابة غير متوقعة للملف {file_path}: {response.status}")
    except urllib.error.HTTPError as e:
        print(f"❌ فشل رفع {file_path}: {e.read().decode()}")

if __name__ == "__main__":
    print("--- محرك أتمتة NAVARIS Sync دقة متناهية ومراجعة ---")
    
    # 🛠️ [الملف 1] كود محرك اللوجستيات والنقل البحري لعلاج وعزل مشاكل موانئ الإسكندرية وأبو قير
    maritime_code = """# engines/maritime_engine.py
# NAVARIS Business Intelligence OS — v20 Maritime & Freight Forwarding Engine

class NavarisMaritimeEngine:
    def __init__(self):
        self.base_freight_rate_20ft = 1200.0
        self.base_freight_rate_40ft = 2200.0

    def calculate_stall_damages(self, delay_days: int, customs_stuck: bool, demurrage_rate_per_day: float) -> dict:
        if delay_days < 0: return {"status": "HOLD", "error": "Negative days."}
        total_demurrage = delay_days * demurrage_rate_per_day
        customs_penalty = 5000.0 if customs_stuck else 0.0
        total_stalled_loss = total_demurrage + customs_penalty
        
        status = "NONE"
        action = "Safe boundaries."
        if total_stalled_loss > 15000.0:
            status = "CRITICAL_STALL"
            action = "Deploy NAVARIS 3rd-Party Integration. Match with qualified customs clearing partners."
            
        return {
            "metrics": {"total_stalled_loss_egp": total_stalled_loss},
            "status": status, "tactical_action": action, "capital_required": 0.0
        }
"""
    push_to_github("engines/maritime_engine.py", maritime_code, "Deploy rigid maritime logic via sync engine")

    # 🛠️ [الملف 2] كود ملف الإعدادات الأوتوماتيكي لإصلاح وعلاج قائمة الـ Actions على متصفح GitHub نهائياً
    pipeline_code = """name: NAVARIS Master Core Automation Pipeline
on:
  workflow_dispatch:
    inputs:
      target_file_path:
        description: 'Specify file path'
        required: true
      file_content:
        description: 'Paste full source code'
        required: true
jobs:
  deploy_artifacts:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: |
          mkdir -p $(dirname "${{ github.event.inputs.target_file_path }}")
          echo "${{ github.event.inputs.file_content }}" > "${{ github.event.inputs.target_file_path }}"
      - run: |
          git config --local user.email "mohamed007hafez@gmail.com"
          git config --local user.name "mohamed007hafez-bit"
          git add .
          git diff-index --quiet HEAD || git commit -m "Automated update via Master Pipeline"
          git push
"""
    push_to_github(".github/workflows/navaris_pipeline.yml", pipeline_code, "Fix master pipeline workflow configuration")
