# image-understand-skill

Claude Code skill for image understanding using Alibaba Cloud Qwen 3.5 Omni Flash vision model.

## Features

- Analyze images with natural language prompts
- Support local files and URLs
- Support JPEG, PNG, GIF, WebP, BMP formats
- OCR text extraction from images
- Multi-image comparison

## Setup

1. Get a DashScope API key from https://dashscope.console.aliyun.com/
2. Set environment variable: `export DASHSCOPE_API_KEY=sk-your-key`
3. Install dependency: `pip install openai`

## Usage

```bash
python scripts/understand_image.py \
  --image "/path/to/image.png" \
  --prompt "Describe what you see"
```

## Installation (Claude Code)

Copy the `image-understand` folder to `~/.claude/skills/` and configure your API key in `~/.claude/settings.json`.
