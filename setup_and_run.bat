@echo off
setlocal
cd /d "%~dp0"

echo ================================================
echo  Graduation Hospital Planner - Setup and Run
echo ================================================
echo Current folder: %CD%
echo.

if not exist "prototype\grid_drag_canvas_app.py" (
  echo [ERROR] prototype\grid_drag_canvas_app.py file not found.
  echo Please unzip the ZIP first, then run this BAT inside the Graduation_Hospital_Planner folder.
  pause
  exit /b 1
)

if not exist "requirements.txt" (
  echo [ERROR] requirements.txt file not found.
  echo Please unzip the full folder again.
  pause
  exit /b 1
)

set "PY_CMD="
py -3 --version >nul 2>&1
if %errorlevel%==0 set "PY_CMD=py -3"

if not defined PY_CMD (
  python --version >nul 2>&1
  if %errorlevel%==0 set "PY_CMD=python"
)

if not defined PY_CMD (
  echo [ERROR] Python 3 was not found on this computer.
  echo Install Python from https://www.python.org/downloads/
  echo IMPORTANT: Check "Add python.exe to PATH" during installation.
  pause
  exit /b 1
)

echo [1/3] Creating local Python virtual environment...
if not exist ".venv\Scripts\python.exe" (
  %PY_CMD% -m venv .venv
  if errorlevel 1 (
    echo [ERROR] Failed to create .venv.
    pause
    exit /b 1
  )
)

echo [2/3] Installing required packages...
".venv\Scripts\python.exe" -m pip install --upgrade pip
if errorlevel 1 (
  echo [ERROR] Failed to upgrade pip.
  pause
  exit /b 1
)

".venv\Scripts\python.exe" -m pip install -r requirements.txt
if errorlevel 1 (
  echo [ERROR] Failed to install required packages.
  pause
  exit /b 1
)

echo [3/3] Starting Streamlit app...
".venv\Scripts\python.exe" -m streamlit run "src\graduation_hospital_planner\grid_drag_canvas_app.py"

pause
