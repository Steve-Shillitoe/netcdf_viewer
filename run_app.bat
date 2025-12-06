@echo off
REM ----------------------------
REM Run Django web app and open browser
REM ----------------------------

REM Set path to Python virtual environment
SET VENV_DIR=venv

REM Activate virtual environment
CALL %VENV_DIR%\Scripts\activate.bat

REM Optional: navigate to project folder (if script is elsewhere)
REM cd /d C:\path\to\netcdf_viewer

REM Start Django server in a separate window
start "" cmd /k "python manage.py runserver"

REM Wait a few seconds for server to start
timeout /t 5 /nobreak >nul

REM Open default web browser to localhost
start http://127.0.0.1:8000/

REM Optional: keep original window open
pause
