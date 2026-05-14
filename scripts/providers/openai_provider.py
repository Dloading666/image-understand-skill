"""OpenAI provider — GPT-4o / GPT-4o-mini / GPT-4-turbo."""

from . import BaseProvider, ProviderConfig, register, load_image

import base64
import os
import sys


@register
class OpenAIProvider(BaseProvider):
    provider_name = "openai"
    provider_env = "OPENAI_API_KEY"
    provider_doc = "OpenAI GPT-4o / GPT-4o-mini"

    DEFAULT_MODEL = "gpt-4o"

    def is_available(self) -> bool:
        return bool(os.environ.get("OPENAI_API_KEY"))

    def analyze(self, images: list[str], prompt: str, config: ProviderConfig) -> str:
        try:
            from openai import OpenAI
        except ImportError:
            print("Error: 'openai' package required. Install: pip install openai", file=sys.stderr)
            sys.exit(1)

        client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

        content = []
        for path in images:
            data, mime = load_image(path)
            b64 = base64.b64encode(data).decode("utf-8")
            content.append({
                "type": "image_url",
                "image_url": {"url": f"data:{mime};base64,{b64}"},
            })
        content.append({"type": "text", "text": prompt})

        try:
            response = client.chat.completions.create(
                model=config.model or self.DEFAULT_MODEL,
                max_tokens=config.max_tokens,
                temperature=config.temperature,
                messages=[{"role": "user", "content": content}],
            )
        except Exception as e:
            print(f"OpenAI API error: {e}", file=sys.stderr)
            sys.exit(1)

        text = response.choices[0].message.content
        if not text:
            print("Error: Empty response from OpenAI", file=sys.stderr)
            sys.exit(1)
        return text
