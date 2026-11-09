@echo off
setlocal
set "ROOT=%~dp0"

where node >nul 2>nul || (
  echo ERROR: Node.js LTS is missing. Install Node.js 20 LTS from https://nodejs.org/ then retry.
  pause
  exit /b 1
)
where npm >nul 2>nul || (
  echo ERROR: npm is missing. Reinstall Node.js LTS with npm enabled.
  pause
  exit /b 1
)

set "PYTHON="
py -3.12 --version >nul 2>nul && set "PYTHON=py -3.12"
if not defined PYTHON py -3.11 --version >nul 2>nul && set "PYTHON=py -3.11"
if not defined PYTHON (
  echo ERROR: Python 3.11 or 3.12 is required for this local setup.
  echo Install Python 3.12 from https://www.python.org/downloads/ and retry.
  pause
  exit /b 1
)

if not exist "%ROOT%.venv\Scripts\python.exe" (
  %PYTHON% -m venv "%ROOT%.venv"
  if errorlevel 1 (
    echo ERROR: Could not create the Python virtual environment.
    pause
    exit /b 1
  )
  "%ROOT%.venv\Scripts\python.exe" -m pip install --upgrade pip
  if errorlevel 1 exit /b 1
  "%ROOT%.venv\Scripts\python.exe" -m pip install -r "%ROOT%requirements.txt"
  if errorlevel 1 exit /b 1
)

if not exist "%ROOT%app\node_modules" (
  pushd "%ROOT%app"
  call npm install
  if errorlevel 1 (
    popd
    echo ERROR: Web dependencies could not be installed.
    pause
    exit /b 1
  )
  popd
)

start "NAVARIS Local API" cmd /k "cd /d ""%ROOT%"" && ""%ROOT%.venv\Scripts\python.exe"" -m backend.main"
start "NAVARIS Client Preview" cmd /k "cd /d ""%ROOT%app"" && call npm run dev"
timeout /t 3 /nobreak >nul
start "" http://localhost:3000

echo NAVARIS local preview is starting.
echo Client website: http://localhost:3000
echo Local API docs: http://127.0.0.1:8000/docs
echo This is a development preview. Do not enter sensitive client or financial data.
endlocal
