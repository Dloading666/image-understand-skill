---
name: image-understand
description: >
  Analyze and understand images using the Alibaba Cloud Qwen 3.5 Omni Flash vision model.
  Use this skill whenever the user wants to: describe, analyze, or extract information from images;
  understand what's in a screenshot, photo, diagram, or chart; compare multiple images;
  read text from images (OCR); identify objects, people, or scenes in images;
  or asks any question about visual content. Even if they don't explicitly say "image understanding"
  or "Qwen", trigger this skill for any image analysis task. Supports local file paths and URLs.
  Supports JPEG, PNG, GIF, WebP, BMP formats.
---

# Image Understanding with Qwen 3.5 Omni Flash

This skill uses the Alibaba Cloud Qwen 3.5 Omni Flash multimodal model to analyze images and return detailed text descriptions. It works by running a Python script that calls the DashScope API (OpenAI-compatible endpoint), sending image data along with the user's question, and printing the model's response.

## Prerequisites

Before using this skill, you **must** configure the API key:

1. Get your DashScope API key from https://dashscope.console.aliyun.com/
2. Set the environment variable `DASHSCOPE_API_KEY` with your key (starts with `sk-`):
   - In your shell: `export DASHSCOPE_API_KEY=sk-your-key-here`
   - Or add it to `~/.claude/settings.json` under `env`:
     ```json
     { "env": { "DASHSCOPE_API_KEY": "sk-your-key-here" } }
     ```
3. Install the Python dependency: `pip install openai`

## How to Use

Run the bundled script via Bash. The script accepts one or more image paths/URLs and a text prompt.

### Single image

```bash
python ~/.claude/skills/image-understand/scripts/understand_image.py \
  --image "/path/to/image.png" \
  --prompt "Describe what you see in this image"
```

### Multiple images (comparison)

```bash
python ~/.claude/skills/image-understand/scripts/understand_image.py \
  --image "/path/to/image1.jpg" \
  --image "/path/to/image2.jpg" \
  --prompt "Compare these two images and describe the differences"
```

### Image from URL

```bash
python ~/.claude/skills/image-understand/scripts/understand_image.py \
  --image "https://example.com/photo.jpg" \
  --prompt "What is shown in this picture?"
```

### Parameters

| Parameter | Required | Default | Description |
|-----------|----------|---------|-------------|
| `--image` | Yes | - | Image path or URL. Repeat for multiple images. |
| `--prompt` | No | "请描述这张图片的内容" | Your question or instruction about the image(s) |
| `--model` | No | `qwen3.5-omni-flash` | Qwen model name |
| `--max-tokens` | No | `4096` | Maximum output tokens. Increase for longer descriptions. |

## Workflow

1. The user provides an image (file path or URL) and a question about it.
2. Translate the user's intent into an appropriate `--prompt` in the language they're using. If they ask in Chinese, write the prompt in Chinese. If in English, use English.
3. Run the script and capture the output.
4. Present the model's response to the user. You may add context or formatting, but do not fabricate content the model did not return.

## Tips

- For detailed analysis, use a longer prompt like "请详细描述这张图片中每个物体的位置、颜色和状态" or "Describe every detail you can see, including text, numbers, and layout."
- For OCR tasks, prompt with "请提取图片中的所有文字" or "Extract all text from this image exactly as it appears."
- If the output is truncated, increase `--max-tokens` (e.g., `--max-tokens 2048`).
- The script prints errors to stderr. If the command fails, check that `DASHSCOPE_API_KEY` is set and valid.
- Other available vision models: `qwen-vl-max` (strongest), `qwen-vl-plus` (cost-effective).
