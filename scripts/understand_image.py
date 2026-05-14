#!/usr/bin/env python3
"""
Multi-provider image understanding tool.

Analyze images using any supported vision model — OpenAI GPT-4o,
Anthropic Claude, Google Gemini, Alibaba Cloud Qwen, or Ollama local models.
Provider is auto-detected from environment variables, or can be chosen explicitly.

Usage:
    # Auto-detect provider (first available API key wins)
    python understand_image.py --image photo.jpg --prompt "What's in this photo?"

    # Explicit provider
    python understand_image.py --provider anthropic --image photo.jpg --prompt "Describe this"

    # Multiple images
    python understand_image.py --image a.jpg --image b.jpg --prompt "Compare these"

    # Custom model
    python understand_image.py --provider openai --model gpt-4o-mini --image photo.jpg --prompt "OCR this"

Environment variables (set at least one):
    OPENAI_API_KEY           → provider: openai
    ANTHROPIC_API_KEY        → provider: anthropic
    GOOGLE_API_KEY           → provider: google
    DASHSCOPE_API_KEY        → provider: alibabacloud
    OLLAMA_HOST              → provider: ollama (default: http://localhost:11434)
"""

import argparse
import sys

# Import all providers so they register themselves in the registry.
# Order doesn't matter — auto_detect checks by priority.
# isort:skip - side-effect imports must come first
import providers.openai_provider        # noqa: F401
import providers.anthropic_provider     # noqa: F401
import providers.google_provider        # noqa: F401
import providers.alibabacloud_provider  # noqa: F401
import providers.ollama_provider        # noqa: F401

from providers import (
    ProviderConfig,
    auto_detect,
    get,
    list_all,
)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Analyze images using any supported vision model.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "Examples:\n"
            "  auto-detect:  %(prog)s --image photo.jpg --prompt \"描述这张图片\"\n"
            "  explicit:     %(prog)s --provider anthropic --image photo.jpg --prompt \"Describe\"\n"
            "  multi-image:  %(prog)s --image a.png --image b.png --prompt \"Compare\"\n"
            "  custom model: %(prog)s --provider openai --model gpt-4o-mini --image img.jpg --prompt \"OCR\"\n"
            "\n"
            f"Available providers: {', '.join(list_all())}"
        ),
    )

    parser.add_argument(
        "--provider",
        choices=list_all(),
        default=None,
        help="Vision provider (default: auto-detect from env vars)",
    )
    parser.add_argument(
        "--image",
        action="append",
        default=None,
        dest="images",
        help="Image path or URL (can be repeated for multi-image analysis)",
    )
    parser.add_argument(
        "--prompt",
        default="请描述这张图片的内容",
        help="Question or instruction about the image(s) (default: Chinese generic prompt)",
    )
    parser.add_argument(
        "--model",
        default=None,
        help="Model name (provider-specific default if omitted)",
    )
    parser.add_argument(
        "--max-tokens",
        type=int,
        default=4096,
        help="Maximum output tokens (default: 4096)",
    )
    parser.add_argument(
        "--temperature",
        type=float,
        default=0.7,
        help="Sampling temperature (default: 0.7)",
    )
    parser.add_argument(
        "--list-providers",
        action="store_true",
        help="List all available providers and exit",
    )
    parser.add_argument(
        "--show-provider",
        action="store_true",
        help="Print which provider/model was used (stderr)",
    )

    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    # --list-providers
    if args.list_providers:
        print("Available providers:")
        for name in list_all():
            p = get(name)
            print(f"  {name:20s}  {p.provider_doc}")
            print(f"  {'':20s}  env: {p.provider_env}")
        sys.exit(0)

    if not args.images:
        parser.error("--image is required (use --list-providers to see available providers)")

    # Resolve provider -------------------------------------------------------
    provider_name = args.provider or auto_detect()
    if not provider_name:
        names = ", ".join(list_all())
        envs = "\n".join(
            f"    {p.provider_env}  →  {name}"
            for name in list_all()
            for p in [get(name)]
        )
        print(
            f"Error: No provider specified and no API keys found.\n"
            f"\n"
            f"Set one of these environment variables:\n{envs}\n"
            f"\n"
            f"Or use --provider to choose from: {names}",
            file=sys.stderr,
        )
        sys.exit(1)

    provider = get(provider_name)

    if not provider.is_available():
        print(
            f"Error: Provider '{provider_name}' selected but {provider.provider_env} is not set.",
            file=sys.stderr,
        )
        sys.exit(1)

    # Build config + run -----------------------------------------------------
    config = ProviderConfig(
        model=args.model or provider.DEFAULT_MODEL,
        max_tokens=args.max_tokens,
        temperature=args.temperature,
    )

    if args.show_provider:
        print(f"[Provider] {provider_name} | Model: {config.model}", file=sys.stderr)

    result = provider.analyze(args.images, args.prompt, config)
    print(result)


if __name__ == "__main__":
    main()
