# image-understand-skill

基于阿里云通义千问视觉模型的 Claude Code 图片理解技能。

## 功能特性

- 自然语言描述和分析图片内容
- 支持本地文件和网络 URL
- 支持 JPEG、PNG、GIF、WebP、BMP 格式
- 图片文字提取（OCR）
- 多图对比分析

## 快速开始

> **使用前必须完成以下配置，否则技能无法运行。**

### 第一步：开通阿里云百炼服务

1. 注册/登录 [阿里云](https://www.aliyun.com/) 账号
2. 前往 [百炼控制台](https://dashscope.console.aliyun.com/) 开通模型服务
3. 进入「API Key 管理」，创建一个 API Key（`sk-` 开头）
4. 确保账户有可用额度（免费额度或付费额度均可）

### 第二步：安装 Python 依赖

```bash
pip install openai
```

### 第三步：配置 API Key

**方式一：写入 Claude Code 配置（推荐，永久生效）**

编辑 `~/.claude/settings.json`，在 `env` 中添加：

```json
{
  "env": {
    "DASHSCOPE_API_KEY": "sk-你的API密钥"
  }
}
```

**方式二：设置环境变量（临时生效）**

```bash
# Linux / macOS
export DASHSCOPE_API_KEY=sk-你的API密钥

# Windows PowerShell
$env:DASHSCOPE_API_KEY="sk-你的API密钥"
```

### 第四步：安装技能到 Claude Code

将本仓库克隆或复制到 `~/.claude/skills/` 目录：

```bash
git clone https://github.com/Dloading666/image-understand-skill.git ~/.claude/skills/image-understand
```

### 验证安装

发送一张图片给 Claude Code，如果能正常返回图片描述，说明配置成功。

## 使用方法

### 单张图片

```bash
python scripts/understand_image.py \
  --image "/path/to/image.png" \
  --prompt "描述这张图片的内容"
```

### 多张图片对比

```bash
python scripts/understand_image.py \
  --image "/path/to/image1.jpg" \
  --image "/path/to/image2.jpg" \
  --prompt "对比这两张图片的区别"
```

### 网络图片

```bash
python scripts/understand_image.py \
  --image "https://example.com/photo.jpg" \
  --prompt "这张图片里有什么？"
```

### 参数说明

| 参数 | 必填 | 默认值 | 说明 |
|------|------|--------|------|
| `--image` | 是 | - | 图片路径或 URL，可多次指定 |
| `--prompt` | 否 | "请描述这张图片的内容" | 对图片的提问或指令 |
| `--model` | 否 | `qwen3.5-omni-flash` | 模型名称 |
| `--max-tokens` | 否 | `4096` | 最大输出 token 数 |

### 其他可用模型

| 模型 | 说明 |
|------|------|
| `qwen-vl-max` | 最强视觉理解能力 |
| `qwen-vl-plus` | 性价比之选 |
| `qwen3.5-omni-flash` | 默认模型，速度快 |

## 提示词技巧

- **详细分析**：`"请详细描述图片中每个物体的位置、颜色和状态"`
- **文字提取**：`"请提取图片中的所有文字"`
- **图片对比**：`"这两张图片有什么不同？"`
- **场景识别**：`"这是在什么地方拍的？"`
