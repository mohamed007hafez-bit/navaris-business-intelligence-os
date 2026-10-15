name: Supervised Python Automation

on:
  push:
    branches: [ "main" ]
  pull_request:
    branches: [ "main" ]
  workflow_dispatch: # تمنحك زراً يدوياً لتشغيل الـ Run في أي وقت تريده

jobs:
  build_and_run:
    runs-on: ubuntu-latest

    steps:
    - name: 1. Fetch Repository Code
      uses: actions/checkout@v4

    - name: 2. Initialize Python Environment
      uses: actions/setup-python@v5
      with:
        python-version: '3.10'
        cache: 'pip' # يقوم بتسريع التشغيل في المرات القادمة عبر كاش المكتبات

    - name: 3. Verify Project Files
      run: |
        echo "=== الأكواد والملفات المتاحة في مشروعك ==="
        ls -la

    - name: 4. Install Requirements
      run: |
        python -m pip install --upgrade pip
        if [ -f requirements.txt ]; then 
          pip install -r requirements.txt
        else
          echo "تنبيه: لم يتم العثور على ملف requirements.txt ل تثبيت المكتبات"
        fi

    - name: 5. Execute Core Application
      run: |
        echo "=== بدء تشغيل البرنامج ==="
        # ملاحظة: إذا كان ملفك الأساسي اسمه مختلف عن main.py قم بتغييره هنا
        if [ -f main.py ]; then
          python main.py
        elif [ -f app.py ]; then
          python app.py
        else
          echo "خطأ: لم نجد ملف main.py أو app.py للتشغيل تلقائياً!"
          exit 1
        fi
