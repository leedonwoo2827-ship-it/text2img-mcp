@echo off
chcp 65001 >nul 2>&1
echo ============================================
echo   text2img-mcp 설치 스크립트
echo ============================================
echo.

REM Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [오류] Python이 설치되어 있지 않습니다.
    echo Python 3.10 이상을 설치해주세요: https://www.python.org/downloads/
    pause
    exit /b 1
)

echo [1/3] 가상환경 생성 중...
if not exist ".venv" (
    python -m venv .venv
)

echo [2/3] 의존성 설치 중...
call .venv\Scripts\activate.bat
pip install -r requirements.txt

echo [3/3] 설치 완료!
echo.
echo ============================================
echo   Claude Desktop 설정 방법
echo ============================================
echo.
echo 1. Claude Desktop 설정 파일을 열어주세요:
echo    %%APPDATA%%\Claude\claude_desktop_config.json
echo.
echo 2. 아래 내용을 mcpServers에 추가하세요:
echo.
echo    "text2img-mcp": {
echo      "command": "%CD%\.venv\Scripts\python.exe",
echo      "args": ["%CD%\server.py"],
echo      "env": {
echo        "GEMINI_API_KEY": "여기에-API키-입력"
echo      }
echo    }
echo.
echo 3. Claude Desktop을 재시작하세요.
echo ============================================
pause
