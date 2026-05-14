---
name: image-understand
description: >
  Multi-provider image understanding skill. Supports OpenAI GPT-4o, Anthropic
  Claude 3.5 Sonnet, Google Gemini, Alibaba Cloud Qwen, and Ollama local models.
  Use for: describing/analyzing images, OCR, screenshot analysis, photo recognition,
  multi-image comparison, extracting information from diagrams/charts, identifying
  objects/people/scenes. Accepts local file paths and URLs. Provider is auto-detected
  from environment variables.
---

# image-understand — Multi-Provider Image Understanding

Analyze images using **any** major vision model — automatically detects which provider's API key you have configured.

Supported providers:

| Provider | Env Variable | Default Model |
|----------|-------------|---------------|
| **OpenAI** | `OPENAI_API_KEY` | `gpt-4o` |
| **Anthropic** | `ANTHROPIC_API_KEY` | `claude-3-5-sonnet-20241022` |
| **Google Gemini** | `GOOGLE_API_KEY` | `gemini-1.5-flash` |
| **Alibaba Cloud (Qwen)** | `DASHSCOPE_API_KEY` | `qwen3.5-omni-flash` |
| **Ollama** (local) | `OLLAMA_HOST` | `llava` |

## Prerequisites

### 1. Install Python dependency

```bash
pip install openai
```

For specific providers, additional packages may be needed:
- **Anthropic**: `pip install anthropic`
- **Google Gemini**: `pip install google-generativeai`
- **Images from URLs**: `pip install httpx` (usually comes with `openai`)

### 2. Set at least one API key

```json
// ~/.claude/settings.json
{
  "env": {
    "OPENAI_API_KEY": "sk-...",
    "ANTHROPIC_API_KEY": "sk-ant-...",
    "GOOGLE_API_KEY": "AIza...",
    "DASHSCOPE_API_KEY": "sk-..."
  }
}
```

Only one key is needed. The tool auto-detects which provider to use.

## Usage

```bash
python ~/.claude/skills/image-understand/scripts/understand_image.py \
  --image "/path/to/photo.jpg" \
  --prompt "描述这张图片"
```

### Provider selection

Auto-detect (no `--provider` flag — first matching env var wins):

```bash
python understand_image.py --image photo.jpg --prompt "Describe this"
```

Explicit provider:

```bash
python understand_image.py --provider anthropic --image photo.jpg --prompt "Describe"
```

### Examples

**OCR / text extraction:**
```bash
python understand_image.py --image scan.png --prompt "提取图片中所有文字，保持原始格式" --show-provider
```

**Multi-image comparison:**
```bash
python understand_image.py \
  --image design-v1.png \
  --image design-v2.png \
  --prompt "Compare these two UI designs and list the differences"
```

**Custom model:**
```bash
python understand_image.py \
  --provider openai --model gpt-4o-mini \
  --image receipt.jpg --prompt "Extract all text from this receipt"
```

### Parameters

| Parameter | Required | Default | Description |
|-----------|----------|---------|-------------|
| `--image` | Yes | - | Image path or URL. Repeat for multiple images. |
| `--prompt` | No | `请描述这张图片的内容` | Question or instruction about the image(s) |
| `--provider` | No | auto-detect | One of: openai, anthropic, google, alibabacloud, ollama |
| `--model` | No | provider default | Override the model name |
| `--max-tokens` | No | `4096` | Maximum output tokens |
| `--temperature` | No | `0.7` | Sampling temperature |
| `--show-provider` | No | off | Print which provider/model was used (to stderr) |
| `--list-providers` | No | off | List all available providers and exit |

## Workflow

1. User provides an image (local file path or URL) and optionally a question.
2. Translate the user's intent into an appropriate `--prompt` in their language.
3. The script auto-detects the provider or uses the one specified.
4. Present the model's response to the user. Add context but do not fabricate content.

## Tips

- **Detailed analysis**: Use long prompts like `"请详细描述图片中每个物体的位置、颜色和状态"`
- **OCR**: `"请提取图片中的所有文字，保持原有格式"`
- **Comparison**: `"Compare the differences between these two images"`
- **Truncated output**: Increase `--max-tokens` (e.g., `--max-tokens 8192`)
- **Debug**: Use `--show-provider` to confirm which model is being called
- **List available providers**: Use `--list-providers`
