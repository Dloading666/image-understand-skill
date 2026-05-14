"""Google Gemini provider — Gemini 1.5 Pro / Gemini 1.5 Flash / Gemini 2.0 Flash."""

from . import BaseProvider, ProviderConfig, register, load_image

import base64
import os
import sys


@register
class GoogleProvider(BaseProvider):
    provider_name = "google"
    provider_env = "GOOGLE_API_KEY"
    provider_doc = "Google Gemini 1.5 Pro / 1.5 Flash / 2.0 Flash"

    DEFAULT_MODEL = "gemini-1.5-flash"

    def is_available(self) -> bool:
        return bool(os.environ.get("GOOGLE_API_KEY"))

    def analyze(self, images: list[str], prompt: str, config: ProviderConfig) -> str:
        try:
            import google.generativeai as genai
        except ImportError:
            print(
                "Error: 'google-generativeai' package required. "
                "Install: pip install google-generativeai",
                file=sys.stderr,
            )
            sys.exit(1)

        genai.configure(api_key=os.environ["GOOGLE_API_KEY"])

        try:
            model = genai.GenerativeModel(
                config.model or self.DEFAULT_MODEL,
                generation_config=genai.types.GenerationConfig(
                    max_output_tokens=config.max_tokens,
                    temperature=config.temperature,
                ),
            )
        except Exception as e:
            print(f"Google API init error: {e}", file=sys.stderr)
            sys.exit(1)

        contents = [prompt]
        for path in images:
            data, mime = load_image(path)
            contents.append({
                "mime_type": mime,
                "data": data,
            })

        try:
            response = model.generate_content(contents)
        except Exception as e:
            print(f"Google API error: {e}", file=sys.stderr)
            sys.exit(1)

        if not response.text:
            # Check for blocked content
            try:
                reason = response.prompt_feedback.block_reason
                print(f"Error: Content blocked by Gemini — {reason}", file=sys.stderr)
            except Exception:
                print("Error: Empty response from Gemini", file=sys.stderr)
            sys.exit(1)

        return response.text
