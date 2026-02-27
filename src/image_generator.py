# -*- coding: utf-8 -*-
import base64
import time
from pathlib import Path

import requests

GEMINI_API_URL = (
    "https://generativelanguage.googleapis.com/v1beta/models/"
    "gemini-2.0-flash-preview-image-generation:generateContent"
)

DEFAULT_IMAGE_DIR = Path.home() / "Documents" / "text2img-mcp" / "images"

VALID_ASPECT_RATIOS = {"1:1", "16:9", "9:16", "4:3", "3:4"}


def generate_image(
    api_key: str,
    prompt: str,
    output_dir: str = "",
    aspect_ratio: str = "1:1",
) -> dict:
    """Gemini API를 호출하여 이미지를 생성하고 파일로 저장한다.

    Returns:
        dict with keys: image_path (str), file_name (str)
    Raises:
        ValueError, RuntimeError on failure
    """
    if not api_key:
        raise ValueError("GEMINI_API_KEY 환경변수가 설정되지 않았습니다.")
    if not prompt.strip():
        raise ValueError("프롬프트가 비어있습니다.")
    if aspect_ratio not in VALID_ASPECT_RATIOS:
        raise ValueError(
            f"지원하지 않는 비율입니다: {aspect_ratio}. "
            f"가능한 값: {', '.join(sorted(VALID_ASPECT_RATIOS))}"
        )

    # Build request
    generation_config: dict = {"responseModalities": ["TEXT", "IMAGE"]}
    if aspect_ratio != "free":
        generation_config["imageConfig"] = {"aspectRatio": aspect_ratio}

    body = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": generation_config,
    }

    headers = {
        "Content-Type": "application/json",
        "x-goog-api-key": api_key,
    }

    resp = requests.post(GEMINI_API_URL, json=body, headers=headers, timeout=120)
    if resp.status_code != 200:
        raise RuntimeError(f"Gemini API 오류 (HTTP {resp.status_code}): {resp.text[:500]}")

    data = resp.json()
    if "error" in data:
        raise RuntimeError(f"Gemini API 오류: {data['error'].get('message', str(data['error']))}")

    # Extract image
    parts = data.get("candidates", [{}])[0].get("content", {}).get("parts", [])
    inline = next((p["inlineData"] for p in parts if "inlineData" in p), None)

    if not inline:
        finish_reason = data.get("candidates", [{}])[0].get("finishReason", "")
        raise RuntimeError(
            f"이미지 데이터가 반환되지 않았습니다. "
            f"{f'(사유: {finish_reason})' if finish_reason else ''}"
        )

    # Save to file
    save_dir = Path(output_dir) if output_dir else DEFAULT_IMAGE_DIR
    save_dir.mkdir(parents=True, exist_ok=True)

    file_name = f"{int(time.time() * 1000)}.png"
    file_path = save_dir / file_name

    image_bytes = base64.b64decode(inline["data"])
    file_path.write_bytes(image_bytes)

    return {
        "image_path": str(file_path.resolve()),
        "file_name": file_name,
    }
