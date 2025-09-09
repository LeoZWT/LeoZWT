@echo off
chcp 65001 >nul
echo Updating GitHub Language Statistics...
echo.

:: Check if Python is installed
set PYTHON_PATH=D:\miniconda3\envs\diive--env\python.exe
if not exist "%PYTHON_PATH%" (
    echo Error: Python not found at specified path
    echo Path: %PYTHON_PATH%
    pause
    exit /b 1
)
echo Found Python at: %PYTHON_PATH%

:: Check if .env file exists
if not exist ".env" (
    echo Error: .env file not found
    echo Please copy .env.example to .env and fill in your GitHub token
    echo.
    echo Get GitHub token: https://github.com/settings/tokens
    echo Required permissions: repo (access private repositories)
    exit /b 1
)

:: Install dependencies
echo Checking dependencies...
"%PYTHON_PATH%" -m pip install requests python-dotenv >nul 2>&1

:: Run generator
echo Generating language statistics SVG...
"%PYTHON_PATH%" generate_lang_stats.py

if %errorlevel% equ 0 (
    echo.
    echo Success! Language statistics updated!
    echo File location: assets\lang-stats-dynamic.svg
) else (
    echo.
    echo Failed! Please check error messages above
)

echo.
pause