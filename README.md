# text2img-mcp

텍스트 프롬프트로 AI 이미지를 생성하는 MCP 서버입니다.
Google Gemini API를 사용하여 제안서, 인포그래픽, 차트 등 비즈니스용 이미지를 생성합니다.

## 설치

### 1. 의존성 설치

```bash
# Windows
install.bat

# 또는 수동 설치
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Gemini API 키 발급

[Google AI Studio](https://aistudio.google.com/apikey)에서 API 키를 발급받으세요.

### 3. Claude Desktop 설정

`%APPDATA%\Claude\claude_desktop_config.json` 파일에 추가:

```json
{
  "mcpServers": {
    "text2img-mcp": {
      "command": "C:\\경로\\text2img-mcp\\.venv\\Scripts\\python.exe",
      "args": ["C:\\경로\\text2img-mcp\\server.py"],
      "env": {
        "GEMINI_API_KEY": "your-api-key"
      }
    }
  }
}
```

Claude Desktop을 재시작하면 `create_proposal_image` 도구를 사용할 수 있습니다.

## MCP Tools

### `create_proposal_image`

텍스트 프롬프트로 이미지를 생성합니다.

| 파라미터 | 타입 | 필수 | 설명 |
|---------|------|-----|------|
| `prompt` | string | O | 이미지 설명 텍스트 |
| `output_dir` | string | X | 저장 디렉토리 (기본: ~/Documents/text2img-mcp/images) |
| `aspect_ratio` | string | X | 비율: `1:1`, `16:9`, `9:16`, `4:3`, `3:4` (기본: `1:1`) |

### `get_image_history`

생성 이력을 조회합니다.

| 파라미터 | 타입 | 필수 | 설명 |
|---------|------|-----|------|
| `limit` | int | X | 조회 개수 (기본: 20) |

## 사용 예시

Claude에게 다음과 같이 요청하세요:

- "2024년 매출 현황 인포그래픽 이미지 만들어줘"
- "프로젝트 일정 간트차트 이미지를 16:9 비율로 생성해줘"
- "이전에 만든 이미지 이력 보여줘"
