"""Alibaba Cloud (DashScope / Qwen) provider — Qwen-VL / Qwen 3.5 Omni Flash."""

from . import BaseProvider, ProviderConfig, register, image_to_base64_data_url

import os
import sys


@register
class AlibabaCloudProvider(BaseProvider):
    provider_name = "alibabacloud"
    provider_env = "DASHSCOPE_API_KEY"
    provider_doc = "Alibaba Cloud Qwen-VL / Qwen 3.5 Omni Flash"

    BASE_URL = "https://dashscope.aliyuncs.com/compatible-mode/v1"
    DEFAULT_MODEL = "qwen3.5-omni-flash"

    def is_available(self) -> bool:
        return bool(os.environ.get("DASHSCOPE_API_KEY"))

    def analyze(self, images: list[str], prompt: str, config: ProviderConfig) -> str:
        try:
            from openai import OpenAI
        except ImportError:
            print("Error: 'openai' package required. Install: pip install openai", file=sys.stderr)
            sys.exit(1)

        client = OpenAI(
            api_key=os.environ["DASHSCOPE_API_KEY"],
            base_url=self.BASE_URL,
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
            print(f"Alibaba Cloud API error: {e}", file=sys.stderr)
            sys.exit(1)

        text = response.choices[0].message.content
        if not text:
            print("Error: Empty response from Qwen model", file=sys.stderr)
            sys.exit(1)
        return text
