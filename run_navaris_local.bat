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
python main.py --demo
if errorlevel 1 (
  echo NAVARIS run failed. Review the error above.
  pause
  exit /b 1
)
echo.
echo NAVARIS workbook created in the output folder.
pause
