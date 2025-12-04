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
echo Next steps:
echo 1. Edit .env and add your GOOGLE_API_KEY from https://aistudio.google.com/app/apikey
echo 2. Activate the virtual environment:
echo      .venv\Scripts\activate
echo 3. Test the installation:
echo      python scripts\test_gemini_integration.py
echo 4. Run your first experiment:
echo      python experiments\recruitment_cv_screening\cv_screener.py
echo.
pause
