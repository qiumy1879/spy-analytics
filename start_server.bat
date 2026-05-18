@echo off
cd /d d:\Desktop\AI-play\spy-analytics\backend
echo.
echo Starting Spy Analytics Server...
echo Activating spy2 virtual environment...
call C:\Users\win10\miniforge3\Scripts\activate.bat C:\Users\win10\miniforge3\envs\spy2
echo Virtual environment activated
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
pause
