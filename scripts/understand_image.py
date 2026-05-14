#!/usr/bin/env python3
"""
Analyze images using Alibaba Cloud Qwen Vision models (DashScope).

Usage:
    python understand_image.py --image photo.jpg --prompt "What's in this photo?"
    python understand_image.py --image a.jpg --image b.jpg --prompt "Compare these"
    python understand_image.py --image https://example.com/photo.jpg --prompt "Describe this"

Environment:
    DASHSCOPE_API_KEY - Required. Get from https://dashscope.console.aliyun.com/
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
    print("Error: 'openai' package required. Install: pip install openai", file=sys.stderr)
    sys.exit(1)

BASE_URL = "https://dashscope.aliyuncs.com/compatible-mode/v1"
DEFAULT_MODEL = "qwen3.5-omni-flash"


def get_client() -> OpenAI:
    api_key = os.environ.get("DASHSCOPE_API_KEY", "")
    if not api_key:
        print("Error: DASHSCOPE_API_KEY is not set.", file=sys.stderr)
        print("Get your API key from https://dashscope.console.aliyun.com/", file=sys.stderr)
        sys.exit(1)
    return OpenAI(api_key=api_key, base_url=BASE_URL)


def load_image(path_or_url: str) -> str:
    """Load an image and return a base64 data URL."""
    if path_or_url.startswith(("http://", "https://")):
        try:
            import httpx
            resp = httpx.get(path_or_url, follow_redirects=True, timeout=30)
            resp.raise_for_status()
            data = resp.content
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
            print(f"Error: Failed to download image: {e}", file=sys.stderr)
            sys.exit(1)
    else:
        p = Path(path_or_url).expanduser().resolve()
        if not p.exists():
            print(f"Error: Image not found: {path_or_url}", file=sys.stderr)
            sys.exit(1)
        suffix = p.suffix.lower().lstrip(".")
        mime_map = {
            "jpg": "image/jpeg", "jpeg": "image/jpeg", "png": "image/png",
            "gif": "image/gif", "webp": "image/webp", "bmp": "image/bmp",
        }
        mime = mime_map.get(suffix, "image/png")
        data = p.read_bytes()

    b64 = base64.b64encode(data).decode("utf-8")
    return f"data:{mime};base64,{b64}"


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Analyze images using Alibaba Cloud Qwen Vision models.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "Examples:\n"
            "  %(prog)s --image photo.jpg --prompt \"描述这张图片\"\n"
            "  %(prog)s --image a.jpg --image b.jpg --prompt \"对比这两张图\"\n"
            "  %(prog)s --image https://example.com/img.jpg --prompt \"Extract text\"\n"
            "  %(prog)s --model qwen-vl-max --image scan.png --prompt \"OCR\""
        ),
    )
    parser.add_argument("--image", action="append", required=True, dest="images",
                        help="Image path or URL (repeat for multiple images)")
    parser.add_argument("--prompt", default="请描述这张图片的内容",
                        help="Question or instruction about the image (default: Chinese generic)")
    parser.add_argument("--model", default=DEFAULT_MODEL,
                        help=f"Model name (default: {DEFAULT_MODEL})")
    parser.add_argument("--max-tokens", type=int, default=4096,
                        help="Max output tokens (default: 4096)")
    parser.add_argument("--temperature", type=float, default=0.7,
                        help="Sampling temperature (default: 0.7)")
    args = parser.parse_args()

    client = get_client()

    content = []
    for path in args.images:
        url = load_image(path.strip())
        content.append({"type": "image_url", "image_url": {"url": url}})
    content.append({"type": "text", "text": args.prompt})

    try:
        response = client.chat.completions.create(
            model=args.model,
            max_tokens=args.max_tokens,
            temperature=args.temperature,
            messages=[{"role": "user", "content": content}],
        )
    except Exception as e:
        print(f"API error: {e}", file=sys.stderr)
        sys.exit(1)

    text = response.choices[0].message.content
    if not text:
        print("Error: Empty response from model", file=sys.stderr)
        sys.exit(1)
    print(text)


if __name__ == "__main__":
    main()
