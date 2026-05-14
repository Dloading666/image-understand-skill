<p align="center">
  <img src="assets/icon.png" alt="image-understand" width="120" />
</p>

<h1 align="center">image-understand-skill</h1>

<p align="center">
  <em>Multi-provider image understanding for Claude Code</em>
</p>

<p align="center">
  <a href="#-features">Features</a> •
  <a href="#-supported-providers">Providers</a> •
  <a href="#-quick-start">Quick Start</a> •
  <a href="#-usage">Usage</a> •
  <a href="#-configuration">Configuration</a> •
  <a href="#-extending">Extending</a>
</p>

---

Analyze images using **any** major vision model — OpenAI GPT-4o, Anthropic Claude,
Google Gemini, Alibaba Cloud Qwen, or local models via Ollama. Provider is
auto-detected from your environment variables.

## ✨ Features

- **Multi-provider** — Bring your own API key, use your preferred model
- **Auto-detection** — No need to specify a provider; the tool picks the first available API key
- **Local & remote images** — Supports file paths and HTTP URLs
- **Multi-image** — Compare multiple images in a single request
- **Extensible** — Add a new provider in ~50 lines of Python
- **Unified CLI** — Same command-line interface regardless of backend

## 🎯 Supported Providers

| Provider | Env Variable | Default Model | SDK |
|----------|-------------|---------------|-----|
| **OpenAI** | `OPENAI_API_KEY` | `gpt-4o` | `openai` |
| **Anthropic** | `ANTHROPIC_API_KEY` | `claude-3-5-sonnet-20241022` | `anthropic` |
| **Google Gemini** | `GOOGLE_API_KEY` | `gemini-1.5-flash` | `google-generativeai` |
| **Alibaba Cloud (Qwen)** | `DASHSCOPE_API_KEY` | `qwen3.5-omni-flash` | `openai` (compatible) |
| **Ollama** (local) | `OLLAMA_HOST` | `llava` | `openai` (compatible) |

## 🚀 Quick Start

### 1. Install

Clone the skill to your Claude Code skills directory:

```bash
git clone https://github.com/Dloading666/image-understand-skill.git \
  ~/.claude/skills/image-understand
```

### 2. Install dependencies

```bash
# Core dependency (always needed)
pip install openai

# Optional — for specific providers:
pip install anthropic       # Only if using Anthropic
pip install google-generativeai  # Only if using Google Gemini
```

### 3. Configure API key

Set **at least one** API key in `~/.claude/settings.json`:

```json
{
  "env": {
    "OPENAI_API_KEY": "sk-...",
    "ANTHROPIC_API_KEY": "sk-ant-...",
    "GOOGLE_API_KEY": "AIza...",
    "DASHSCOPE_API_KEY": "sk-..."
  }
}
```

### 4. Use it

```bash
python ~/.claude/skills/image-understand/scripts/understand_image.py \
  --image ~/Desktop/photo.jpg \
  --prompt "What's in this photo?"
```

That's it. The tool will auto-detect which API key you have set and use the
corresponding provider.

## 📖 Usage

### Basic

```bash
python understand_image.py --image photo.jpg --prompt "描述这张图片"
```

### Explicit provider

```bash
python understand_image.py \
  --provider anthropic \
  --image screenshot.png \
  --prompt "Describe what you see in this screenshot"
```

### Multi-image comparison

```bash
python understand_image.py \
  --image mockup-v1.png \
  --image mockup-v2.png \
  --prompt "Compare these two designs in detail"
```

### OCR

```bash
python understand_image.py \
  --provider openai \
  --model gpt-4o-mini \
  --image scanned-document.jpg \
  --prompt "Extract all text exactly as it appears, preserving formatting"
```

### List available providers

```bash
python understand_image.py --list-providers
```

### All parameters

| Parameter | Required | Default | Description |
|-----------|----------|---------|-------------|
| `--image` | Yes | - | Image path or URL. Repeat for multiple images. |
| `--prompt` | No | `请描述这张图片的内容` | Question or instruction about the image(s) |
| `--provider` | No | auto-detect | `openai`, `anthropic`, `google`, `alibabacloud`, `ollama` |
| `--model` | No | provider default | Override the model name |
| `--max-tokens` | No | `4096` | Maximum output tokens |
| `--temperature` | No | `0.7` | Sampling temperature |
| `--show-provider` | No | off | Print provider + model used (to stderr) |
| `--list-providers` | No | off | List all available providers and exit |

## ⚙️ How Auto-Detection Works

When `--provider` is not specified, the tool checks environment variables in
this order and picks the first one that is set:

1. `ANTHROPIC_API_KEY` → Anthropic Claude
2. `OPENAI_API_KEY` → OpenAI
3. `GOOGLE_API_KEY` → Google Gemini
4. `DASHSCOPE_API_KEY` → Alibaba Cloud Qwen
5. `OLLAMA_HOST` → Ollama (local)

To override, pass `--provider` explicitly.

## 🧩 Architecture

```
scripts/
├── understand_image.py        # Entry point — CLI parsing, provider dispatch
└── providers/
    ├── __init__.py             # Base class, registry, image helpers
    ├── openai_provider.py      # OpenAI GPT-4o
    ├── anthropic_provider.py   # Anthropic Claude
    ├── google_provider.py      # Google Gemini
    ├── alibabacloud_provider.py # Alibaba Cloud Qwen
    └── ollama_provider.py      # Ollama (local)
```

Adding a new provider is straightforward:

1. Create `providers/your_provider.py`
2. Subclass `BaseProvider`, implement `is_available()` and `analyze()`
3. Decorate with `@BaseProvider.register`
4. Import it in `understand_image.py`

## 🔧 Tips

| Goal | Suggestion |
|------|------------|
| Detailed scene description | Use a long prompt: *"Describe every object, its position, color, and relationship to other objects"* |
| OCR / text extraction | *"Extract all text from this image exactly as it appears, preserving line breaks and formatting"* |
| Screenshot analysis | *"Describe the UI layout, list all visible elements and their states"* |
| Image comparison | *"Compare these images and list all differences in detail"* |
| Debug which model runs | Pass `--show-provider` |
| Truncated output | Increase `--max-tokens 8192` |

## 📄 License

MIT
