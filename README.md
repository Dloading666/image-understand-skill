# image-understand-skill

基于阿里云通义千问视觉模型的 Claude Code 图片理解技能。

## 功能特性

- 自然语言描述和分析图片内容
- 支持本地文件和网络 URL
- 支持 JPEG、PNG、GIF、WebP、BMP 格式
- 图片文字提取（OCR）
- 多图对比分析
- 支持 `qwen3.5-omni-flash`、`qwen-vl-max`、`qwen-vl-plus` 等模型

## 快速开始

### 第一步：开通阿里云百炼服务

1. 注册/登录 [阿里云](https://www.aliyun.com/) 账号
2. 前往 [百炼控制台](https://dashscope.console.aliyun.com/) 开通模型服务
3. 进入「API Key 管理」，创建一个 API Key（`sk-` 开头）
4. 确保账户有可用额度

### 第二步：安装 Python 依赖

```bash
pip install openai
```

### 第三步：配置 API Key

**推荐（永久生效）：** 编辑 `~/.claude/settings.json`：

```json
{
  "env": {
    "DASHSCOPE_API_KEY": "sk-你的API密钥"
  }
}
```

**临时使用：**
```bash
# Windows PowerShell
$env:DASHSCOPE_API_KEY="sk-你的API密钥"

# Linux / macOS
export DASHSCOPE_API_KEY=sk-你的API密钥
```

### 第四步：安装技能

```bash
git clone https://github.com/Dloading666/image-understand-skill.git ~/.claude/skills/image-understand
```

### 验证安装

发送一张图片给 Claude Code，如果能正常返回图片描述，说明配置成功。

## 使用方法

### 单张图片

```bash
python ~/.claude/skills/image-understand/scripts/understand_image.py \
  --image "/path/to/image.png" \
  --prompt "描述这张图片的内容"
```

### 多张图片对比

```bash
python ~/.claude/skills/image-understand/scripts/understand_image.py \
  --image "/path/to/image1.jpg" \
  --image "/path/to/image2.jpg" \
  --prompt "对比这两张图片的区别"
```

### 网络图片

```bash
python ~/.claude/skills/image-understand/scripts/understand_image.py \
  --image "https://example.com/photo.jpg" \
  --prompt "这张图片里有什么？"
```

### 参数说明

| 参数 | 必填 | 默认值 | 说明 |
|------|------|--------|------|
| `--image` | 是 | - | 图片路径或 URL，可多次指定 |
| `--prompt` | 否 | `请描述这张图片的内容` | 对图片的提问或指令 |
| `--model` | 否 | `qwen3.5-omni-flash` | 模型名称 |
| `--max-tokens` | 否 | `4096` | 最大输出 token 数 |
| `--temperature` | 否 | `0.7` | 采样温度 |

### 可选模型

| 模型 | 说明 |
|------|------|
| `qwen3.5-omni-flash` | 默认，速度快 |
| `qwen-vl-max` | 最强视觉理解能力 |
| `qwen-vl-plus` | 性价比之选 |

## 提示词技巧

- **详细分析**：`"请详细描述图片中每个物体的位置、颜色和状态"`
- **文字提取**：`"请提取图片中的所有文字，保持原有格式"`
- **图片对比**：`"这两张图片有什么不同？"`
- **场景识别**：`"这是在什么地方拍的？"`
