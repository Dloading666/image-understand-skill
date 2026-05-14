"""
Alibaba Cloud Qwen Vision Script

Calls the Qwen 3.5 Omni Flash model via DashScope's OpenAI-compatible API
to analyze one or more images and return a text description.

Usage:
    python understand_image.py --image <path_or_url> [--image ...] --prompt <text> [--model <model>] [--max-tokens <n>]

Environment:
    DASHSCOPE_API_KEY  - Required. Your DashScope API key (sk-... format).
                         Get one from https://dashscope.console.aliyun.com/
"""

import argparse
import base64
import os
import sys
from pathlib import Path

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

try:
    from openai import OpenAI
except ImportError:
    print("Error: 'openai' package is required. Install with: pip install openai", file=sys.stderr)
    sys.exit(1)

BASE_URL = "https://dashscope.aliyuncs.com/compatible-mode/v1"
DEFAULT_MODEL = "qwen3.5-omni-flash"


def get_client() -> OpenAI:
    api_key = os.environ.get("DASHSCOPE_API_KEY", "")
    if not api_key:
        print("Error: DASHSCOPE_API_KEY environment variable is not set.", file=sys.stderr)
        print("Get your API key from https://dashscope.console.aliyun.com/", file=sys.stderr)
        sys.exit(1)
    return OpenAI(api_key=api_key, base_url=BASE_URL)


def image_to_base64_url(image_path: str) -> str:
    """Convert image to data URL (base64). Works for both local files and HTTP URLs."""
    if image_path.startswith(("http://", "https://")):
        try:
            import httpx
            resp = httpx.get(image_path, follow_redirects=True, timeout=30)
            resp.raise_for_status()
            data = resp.content
            # Guess mime from content-type header or URL
            ct = resp.headers.get("content-type", "")
            if "png" in ct:
                mime = "image/png"
            elif "webp" in ct:
                mime = "image/webp"
            elif "gif" in ct:
                mime = "image/gif"
            else:
                mime = "image/jpeg"
        except Exception as e:
            print(f"Error: Failed to download image from {image_path}: {e}", file=sys.stderr)
            sys.exit(1)
    else:
        p = Path(image_path).expanduser().resolve()
        if not p.exists():
            print(f"Error: Image file not found: {image_path}", file=sys.stderr)
            sys.exit(1)
        suffix = p.suffix.lower().lstrip(".")
        mime_map = {
            "jpg": "jpeg", "jpeg": "jpeg", "png": "png",
            "gif": "gif", "webp": "webp", "bmp": "bmp",
        }
        mime = f"image/{mime_map.get(suffix, 'png')}"
        data = p.read_bytes()

    b64 = base64.b64encode(data).decode()
    return f"data:{mime};base64,{b64}"


def main():
    parser = argparse.ArgumentParser(description="Analyze images using Qwen Vision (DashScope)")
    parser.add_argument("--image", action="append", required=True, help="Image path or URL (can be repeated)")
    parser.add_argument("--prompt", default="请描述这张图片的内容", help="Question or instruction about the images")
    parser.add_argument("--model", default=DEFAULT_MODEL, help=f"Model name (default: {DEFAULT_MODEL})")
    parser.add_argument("--max-tokens", type=int, default=4096, help="Max output tokens (default: 4096)")
    args = parser.parse_args()

    client = get_client()

    content = []
    for path in args.image:
        url = image_to_base64_url(path.strip())
        content.append({"type": "image_url", "image_url": {"url": url}})
    content.append({"type": "text", "text": args.prompt})

    try:
        response = client.chat.completions.create(
            model=args.model,
            max_tokens=args.max_tokens,
            messages=[{"role": "user", "content": content}],
        )
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

    if response.choices and response.choices[0].message.content:
        print(response.choices[0].message.content)
    else:
        print("No text content in response.", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
