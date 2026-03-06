@echo off
chcp 949 >nul 2>&1
echo ============================================
echo   text2img-mcp Install Script
echo ============================================
echo.

REM Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [Error] Python is not installed.
    echo Please install Python 3.10+: https://www.python.org/downloads/
    pause
    exit /b 1
)

echo [1/3] Creating virtual environment...
if not exist ".venv" (
    python -m venv .venv
)

echo [2/3] Installing dependencies...
call .venv\Scripts\activate.bat
pip install -r requirements.txt

echo [3/3] Installation complete!
echo.
echo ============================================
echo   Claude Desktop Configuration
echo ============================================
echo.
echo 1. Open Claude Desktop config file:
echo    %%APPDATA%%\Claude\claude_desktop_config.json
echo.
echo 2. Add the following to mcpServers:
echo.
echo    {
echo      "text2img-mcp": {
echo        "command": "%CD%\.venv\Scripts\python.exe",
echo        "args": ["%CD%\server.py"],
echo        "env": {
echo          "GEMINI_API_KEY": "YOUR-API-KEY-HERE"
echo        }
echo      }
echo    }
echo.
echo 3. Restart Claude Desktop.
echo ============================================
pause
