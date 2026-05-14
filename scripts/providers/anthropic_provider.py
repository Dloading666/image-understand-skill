"""Anthropic provider — Claude 3.5 Sonnet / Claude 3 Opus / Claude 3.5 Haiku."""

from . import BaseProvider, ProviderConfig, register, load_image

import base64
import os
import sys


@register
class AnthropicProvider(BaseProvider):
    provider_name = "anthropic"
    provider_env = "ANTHROPIC_API_KEY"
    provider_doc = "Anthropic Claude 3.5 Sonnet / Claude 3 Opus / Claude 3 Haiku"

    DEFAULT_MODEL = "claude-3-5-sonnet-20241022"

    def is_available(self) -> bool:
        return bool(os.environ.get("ANTHROPIC_API_KEY"))

    def analyze(self, images: list[str], prompt: str, config: ProviderConfig) -> str:
        try:
            from anthropic import Anthropic
        except ImportError:
            print("Error: 'anthropic' package required. Install: pip install anthropic", file=sys.stderr)
            sys.exit(1)

        client = Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])

        content = []
        for path in images:
            data, mime = load_image(path)
            b64 = base64.b64encode(data).decode("utf-8")
            content.append({
                "type": "image",
                "source": {
                    "type": "base64",
                    "media_type": mime,
                    "data": b64,
                },
            })
        content.append({"type": "text", "text": prompt})

        try:
            response = client.messages.create(
                model=config.model or self.DEFAULT_MODEL,
                max_tokens=config.max_tokens,
                temperature=config.temperature,
                messages=[{"role": "user", "content": content}],
            )
        except Exception as e:
            print(f"Anthropic API error: {e}", file=sys.stderr)
            sys.exit(1)

        text = "".join(block.text for block in response.content if block.type == "text")
        if not text:
            print("Error: Empty response from Anthropic", file=sys.stderr)
            sys.exit(1)
        return text
