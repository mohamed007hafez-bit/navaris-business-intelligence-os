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
  echo NAVARIS demo run failed. Review the error above.
  pause
  exit /b 1
)
python suco_quote_workbook.py --output "output\navaris-quote-suco-aog-500kg.xlsx"
if errorlevel 1 (
  echo NAVARIS quote template generation failed. Review the error above.
  pause
  exit /b 1
)
if not exist "output\navaris-quote-demo.xlsx" (
  echo ERROR: demo workbook was not created.
  pause
  exit /b 1
)
if not exist "output\navaris-quote-suco-aog-500kg.xlsx" (
  echo ERROR: quote template was not created.
  pause
  exit /b 1
)
echo.
echo SUCCESS: both Excel files exist in output.
echo NOTE: the demo workbook is illustrative; the AOG workbook is an unpriced template, not a commercial offer.
pause
