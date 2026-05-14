"""
Multi-provider image understanding framework.

Supports OpenAI, Anthropic, Google Gemini, Alibaba Cloud (Qwen), Ollama,
and any OpenAI-compatible API — all through a unified CLI interface.
"""

import base64
import os
import sys
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional


# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

@dataclass
class ProviderConfig:
    """Per-call configuration passed to every provider."""
    model: str
    max_tokens: int = 4096
    temperature: float = 0.7
    extra: dict = field(default_factory=dict)   # Provider-specific knobs


# ---------------------------------------------------------------------------
# Abstract base
# ---------------------------------------------------------------------------

class BaseProvider(ABC):
    """A provider knows how to call one family of vision models.

    Subclasses override ``provider_name`` and ``provider_env`` as class
    attributes so the registry can auto-detect them without instantiation.
    """

    provider_name: str = ""
    provider_env: str = ""        # Primary env-var checked by auto_detect
    provider_doc: str = ""        # Short description shown in --help

    @abstractmethod
    def is_available(self) -> bool:
        """Return True when the required credentials are present."""

    @abstractmethod
    def analyze(self, images: list[str], prompt: str, config: ProviderConfig) -> str:
        """Send *images* (local paths or URLs) + *prompt* and return a text response.

        Each provider is responsible for reading / downloading images in the
        way its SDK expects (base64 inline, URL passthrough, etc.).
        """


# ---------------------------------------------------------------------------
# Registry
# ---------------------------------------------------------------------------

_registry: dict[str, type[BaseProvider]] = {}


def register(cls: type[BaseProvider]) -> type[BaseProvider]:
    """Decorator that registers a provider class."""
    _registry[cls.provider_name] = cls
    return cls


def get(name: str) -> BaseProvider:
    """Instantiate a registered provider by name."""
    if name not in _registry:
        names = ", ".join(_registry)
        raise ValueError(f"Unknown provider '{name}'. Available: {names}")
    return _registry[name]()


def auto_detect() -> Optional[str]:
    """Return the first provider whose primary env-var is set (priority order)."""
    for name, cls in _registry.items():
        env_var = cls.provider_env
        if env_var and os.environ.get(env_var):
            return name
    return None


def list_all() -> list[str]:
    return list(_registry.keys())


# ---------------------------------------------------------------------------
# Shared image helpers
# ---------------------------------------------------------------------------

def _read_local_image(path: str) -> tuple[bytes, str]:
    """Read a local image file → (raw_bytes, mime_type)."""
    p = Path(path).expanduser().resolve()
    if not p.exists():
        print(f"Error: Image file not found: {path}", file=sys.stderr)
        sys.exit(1)

    suffix = p.suffix.lower().lstrip(".")
    mime_map = {
        "jpg": "image/jpeg", "jpeg": "image/jpeg",
        "png": "image/png", "gif": "image/gif",
        "webp": "image/webp", "bmp": "image/bmp",
    }
    mime = mime_map.get(suffix, "image/png")
    return p.read_bytes(), mime


def _download_image(url: str) -> tuple[bytes, str]:
    """Download a remote image → (raw_bytes, mime_type)."""
    try:
        import httpx
        resp = httpx.get(url, follow_redirects=True, timeout=30)
        resp.raise_for_status()
        ct = resp.headers.get("content-type", "")
        if "png" in ct:
            mime = "image/png"
        elif "webp" in ct:
            mime = "image/webp"
        elif "gif" in ct:
            mime = "image/gif"
        else:
            mime = "image/jpeg"
        return resp.content, mime
    except Exception as e:
        print(f"Error: Failed to download image from {url}: {e}", file=sys.stderr)
        sys.exit(1)


def load_image(path_or_url: str) -> tuple[bytes, str]:
    """Load an image from a local path or URL → (raw_bytes, mime_type)."""
    if path_or_url.startswith(("http://", "https://")):
        return _download_image(path_or_url)
    return _read_local_image(path_or_url)


def image_to_base64_data_url(path_or_url: str) -> str:
    """Load an image and encode it as a ``data:`` URL (OpenAI-style)."""
    data, mime = load_image(path_or_url)
    b64 = base64.b64encode(data).decode("utf-8")
    return f"data:{mime};base64,{b64}"
