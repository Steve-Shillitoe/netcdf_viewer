@echo off
REM Activate virtual environment (adjust path if yours is different)
call venv\Scripts\activate.bat

echo Running all Django tests...
python manage.py test

echo Running tests for uploader app with detailed output...
python manage.py test uploader --verbosity 2

REM Deactivate virtual environment
deactivate

echo.
echo Tests complete. Press any key to exit...
pause
