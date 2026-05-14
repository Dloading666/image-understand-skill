"""Ollama provider — local vision models (llava, bakllava, minicpm-v, etc.)."""

from . import BaseProvider, ProviderConfig, register, image_to_base64_data_url

import os
import sys


@register
class OllamaProvider(BaseProvider):
    provider_name = "ollama"
    provider_env = "OLLAMA_HOST"
    provider_doc = "Ollama local models (llava, bakllava, minicpm-v, etc.)"

    DEFAULT_MODEL = "llava"

    def is_available(self) -> bool:
        host = os.environ.get("OLLAMA_HOST", "http://localhost:11434")
        return bool(host)

    def analyze(self, images: list[str], prompt: str, config: ProviderConfig) -> str:
        try:
            from openai import OpenAI
        except ImportError:
            print("Error: 'openai' package required. Install: pip install openai", file=sys.stderr)
            sys.exit(1)

        host = os.environ.get("OLLAMA_HOST", "http://localhost:11434")
        client = OpenAI(
            api_key="ollama",  # Ollama ignores the key
            base_url=f"{host.rstrip('/')}/v1",
        )

        content = []
        for path in images:
            content.append({
                "type": "image_url",
                "image_url": {"url": image_to_base64_data_url(path)},
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
            print(f"Ollama error: {e}", file=sys.stderr)
            sys.exit(1)

        text = response.choices[0].message.content
        if not text:
            print("Error: Empty response from Ollama", file=sys.stderr)
            sys.exit(1)
        return text
