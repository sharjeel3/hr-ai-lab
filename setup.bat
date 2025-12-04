@echo off
REM Setup script for HR AI Lab (Windows)

echo Setting up HR AI Lab...

REM Check if .venv exists
if exist ".venv" (
    echo Virtual environment already exists
) else (
    echo Creating virtual environment...
    python -m venv .venv
    echo Virtual environment created
)

REM Activate virtual environment
echo Activating virtual environment...
call .venv\Scripts\activate.bat

REM Upgrade pip
echo Upgrading pip...
python -m pip install --upgrade pip

REM Install dependencies
echo Installing dependencies...
pip install -r requirements.txt

REM Check for .env file
if exist ".env" (
    echo .env file already exists
) else (
    echo Creating .env from template...
    copy .env.example .env
    echo Please edit .env and add your API keys
)

echo.
echo Setup complete!
echo.
echo To activate the virtual environment in the future, run:
echo   .venv\Scripts\activate
echo.
echo To run an experiment:
echo   python scripts\run_experiment.py --experiment cv_screening
echo.
pause
