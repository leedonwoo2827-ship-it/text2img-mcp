# -*- coding: utf-8 -*-
import os
import sys
from pathlib import Path

BASE_DIR = Path(__file__).parent
sys.path.insert(0, str(BASE_DIR / "src"))

from mcp.server.fastmcp import FastMCP
from image_generator import generate_image
from db import init_db, save_generation, get_generations

# Initialize DB on startup
init_db()

mcp = FastMCP("text2img-mcp")


@mcp.tool()
def create_proposal_image(
    prompt: str,
    output_dir: str = "",
    aspect_ratio: str = "1:1",
) -> str:
    """텍스트 프롬프트로 AI 이미지를 생성합니다 (Gemini API 사용).

    제안서, 인포그래픽, 차트, 슬라이드 등 비즈니스용 이미지를 텍스트 설명만으로 생성합니다.

    Args:
        prompt: 생성할 이미지에 대한 텍스트 설명 (예: "2024년 매출 현황 인포그래픽")
        output_dir: 이미지 저장 디렉토리 경로 (기본: ~/Documents/text2img-mcp/images)
        aspect_ratio: 이미지 비율 - "1:1", "16:9", "9:16", "4:3", "3:4" (기본: "1:1")

    Returns:
        생성된 이미지 파일의 절대경로와 메타데이터
    """
    api_key = os.environ.get("GEMINI_API_KEY", "")

    try:
        result = generate_image(
            api_key=api_key,
            prompt=prompt,
            output_dir=output_dir,
            aspect_ratio=aspect_ratio,
        )

        # Save metadata to SQLite
        gen_id = save_generation(
            prompt=prompt,
            image_path=result["image_path"],
            aspect_ratio=aspect_ratio,
        )

        return (
            f"이미지가 성공적으로 생성되었습니다.\n"
            f"파일 경로: {result['image_path']}\n"
            f"파일명: {result['file_name']}\n"
            f"비율: {aspect_ratio}\n"
            f"기록 ID: {gen_id}"
        )

    except (ValueError, RuntimeError) as e:
        return f"오류: {e}"
    except Exception as e:
        return f"오류: {type(e).__name__}: {e}"


@mcp.tool()
def get_image_history(limit: int = 20) -> str:
    """이전에 생성한 이미지 이력을 조회합니다.

    Args:
        limit: 조회할 최대 개수 (기본: 20)

    Returns:
        생성 이력 목록 (프롬프트, 파일경로, 생성일시)
    """
    try:
        records = get_generations(limit=limit)
        if not records:
            return "생성 이력이 없습니다."

        lines = [f"최근 {len(records)}건의 이미지 생성 이력:\n"]
        for r in records:
            lines.append(
                f"- [{r['created_at']}] {r['prompt'][:60]}\n"
                f"  경로: {r['image_path']}\n"
                f"  비율: {r['aspect_ratio']}"
            )
        return "\n".join(lines)

    except Exception as e:
        return f"오류: {type(e).__name__}: {e}"


if __name__ == "__main__":
    mcp.run()
