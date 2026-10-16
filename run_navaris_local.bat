@echo off
setlocal
cd /d "%~dp0"
if not exist ".venv\Scripts\python.exe" (
  py -3 -m venv .venv
  call .venv\Scripts\activate
  python -m pip install --upgrade pip
  pip install -r requirements.txt
) else (
  call .venv\Scripts\activate
)
python main.py --demo --output "output\navaris-quote-demo.xlsx"
if errorlevel 1 (
  echo NAVARIS run failed. Review the error above.
  pause
  exit /b 1
)
if not exist "output\navaris-quote-demo.xlsx" (
  echo ERROR: expected workbook was not created.
  pause
  exit /b 1
)
echo.
echo SUCCESS: output\navaris-quote-demo.xlsx exists.
echo NOTE: this is a demo workbook, not a priced commercial offer.
pause
