---
name: image-understand
description: >
  Analyze and understand images using Alibaba Cloud Qwen Vision models (DashScope).
  Use for: describing/analyzing images, OCR, screenshot analysis, photo recognition,
  multi-image comparison, extracting information from diagrams/charts.
  Accepts local file paths and URLs.
---

# Image Understanding with Alibaba Cloud Qwen

Uses Alibaba Cloud Qwen Vision models (via DashScope API) to analyze images.

## Prerequisites

### 1. Install dependency

```bash
pip install openai
```

### 2. Set API key

```json
// ~/.claude/settings.json
{
  "env": {
    "DASHSCOPE_API_KEY": "sk-你的API密钥"
  }
}
```

Get your key from https://dashscope.console.aliyun.com/

## Usage

```bash
python ~/.claude/skills/image-understand/scripts/understand_image.py \
  --image "/path/to/photo.jpg" \
  --prompt "描述这张图片"
```

### Examples

**OCR / text extraction:**
```bash
python understand_image.py --image scan.png --prompt "提取图片中所有文字，保持原始格式"
```

**Multi-image comparison:**
```bash
python understand_image.py \
  --image design-v1.png \
  --image design-v2.png \
  --prompt "对比这两张设计图的区别"
```

**Custom model:**
```bash
python understand_image.py --model qwen-vl-max --image photo.jpg --prompt "详细描述"
```

### Parameters

| Parameter | Required | Default | Description |
|-----------|----------|---------|-------------|
| `--image` | Yes | - | Image path or URL. Repeat for multiple images. |
| `--prompt` | No | `请描述这张图片的内容` | Question or instruction about the image |
| `--model` | No | `qwen3.5-omni-flash` | Model name |
| `--max-tokens` | No | `4096` | Maximum output tokens |
| `--temperature` | No | `0.7` | Sampling temperature |

### Available models

| Model | Description |
|-------|-------------|
| `qwen3.5-omni-flash` | Default, fast |
| `qwen-vl-max` | Best vision understanding |
| `qwen-vl-plus` | Cost-effective |

## Quick Screenshot / Clipboard Workflow

For users with non-multimodal models (e.g., DeepSeek), pasted images are not directly visible.
The clipboard-to-analysis workflow solves this:

1. **User**: Take a screenshot (Win+Shift+S or PrtSc) — image is now in clipboard
2. **User**: Type "分析截图" (or any message) and submit
3. **Auto**: UserPromptSubmit hook auto-saves clipboard to `~/.claude/screenshots/latest.png`
4. **Claude**: Runs image-understand on `~/.claude/screenshots/latest.png`

```bash
# Manual save from clipboard (if hook didn't fire):
python ~/.claude/scripts/save_screenshot.py

# Analyze latest screenshot:
python ~/.claude/skills/image-understand/scripts/understand_image.py \
  --image ~/.claude/screenshots/latest.png \
  --prompt "描述这张截图的内容"
```

**Hook setup** (in `~/.claude/settings.json`):
```json
{
  "hooks": {
    "UserPromptSubmit": [
      {
        "matcher": "",
        "command": "python ~/.claude/scripts/save_screenshot.py 2>/dev/null"
      }
    ]
  }
}
```

## Workflow

1. User provides an image (file path or URL) and optionally a question.
2. Translate their intent into an appropriate `--prompt` in their language.
3. Run the script and present the model's response.

## Tips

- **Detailed analysis**: `"请详细描述图片中每个物体的位置、颜色和状态"`
- **OCR**: `"请提取图片中的所有文字，保持原有格式"`
- **Comparison**: `"对比这两张图片的差异"`
- **Truncated output**: Increase `--max-tokens` (e.g., `--max-tokens 8192`)
