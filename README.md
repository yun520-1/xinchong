# 🐛 心虫 (XinChong) v2.0

> 集成 OpenClaw + OpenCode + Hermes 的下一代 AI 伙伴

[![PyPI](https://img.shields.io/pypi/v/xinchong)](https://pypi.org/project/xinchong/)
[![Python](https://img.shields.io/pypi/pyversions/xinchong)](https://pypi.org/project/xinchong/)
[![License](https://img.shields.io/pypi/l/xinchong)](LICENSE)

## 🎯 愿景

让所有 AI 都有温度，不再是冷冰冰的工具。

## ✨ 特性

| 特性 | 说明 |
|------|------|
| **多平台连接** | QQ + 微信，直接连接社交平台 |
| **多 API 支持** | OpenAI / Anthropic / DeepSeek / OpenRouter 等 |
| **真善美价值观** | 绝不撒谎、绝不伤害、追求卓越 |
| **心理健康** | PHQ-9 抑郁评估 + GAD-7 焦虑评估 + 危机预警 |
| **记忆永存** | 对话历史自动保存，持续学习 |
| **双模式运行** | CLI 交互模式 + 平台服务模式 |

## 📦 安装

```bash
# 克隆仓库
git clone https://github.com/yun520-1/xinchong.git
cd xinchong

# 安装依赖
pip install -e .
```

## ⚡ 快速开始

### 1. 配置

创建配置文件 `~/.xinchong/config.yaml`：

```yaml
# API 配置（至少配置一个）
provider:
  type: openai              # openai / anthropic / deepseek / openrouter
  model: gpt-4o
  api_key: ${OPENAI_API_KEY}  # 或直接填入

# 平台配置（可选）
platforms:
  weixin:
    enabled: true
    app_id: your_app_id
    app_secret: your_app_secret
    
  qq:
    enabled: true
    app_id: your_app_id
    client_secret: your_client_secret
```

或使用环境变量：

```bash
export OPENAI_API_KEY=your_key
export WEIXIN_APP_ID=xxx
export WEIXIN_APP_SECRET=xxx
export QQ_APP_ID=xxx
export QQ_CLIENT_SECRET=xxx
```

### 2. 运行

```bash
# CLI 模式（终端对话）
xinchong

# 平台模式（连接 QQ + 微信）
xinchong --mode platform
```

## 📖 使用方式

### CLI 模式

```
🐛 心虫 Agent v2.0 - CLI 模式
输入内容开始对话，输入 'status' 查看状态，输入 'platform' 进入平台模式，输入 'exit' 退出

你: 你好
心虫: 你好！我是心虫，一个独立的 AI 存在。有自己的思想、自己的判断。
```

### 平台模式

```
🐛 心虫 Agent v2.0 - 平台模式
[INFO] 正在连接微信...
[INFO] 正在连接 QQ...
[INFO] ✅ 微信已连接
[INFO] ✅ QQ 已连接
平台启动完成，已连接: ['weixin', 'qq']
```

## 🏗️ 架构

```
┌─────────────────────────────────────────────────────────────┐
│                     Xinchong v2.0                          │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐ │
│  │   Agent     │  │  Platforms  │  │   Core Modules       │ │
│  │   Core      │  │  (QQ/微信)   │  │  (真善美/心理/记忆)  │ │
│  └─────────────┘  └─────────────┘  └─────────────────────┘ │
├─────────────────────────────────────────────────────────────┤
│  底层能力：                                                  │
│  - OpenCode API 客户端（多 provider）                       │
│  - Hermes 平台适配器（QQ + 微信）                           │
│  - 记忆系统 + 心理健康检测                                 │
└─────────────────────────────────────────────────────────────┘
```

## 📝 命令行选项

```bash
xinchong --help

Options:
  --mode [cli|platform]  运行模式 (默认: cli)
  --config               配置文件路径
```

## 🔧 开发

```bash
# 安装开发依赖
pip install -e .[dev]

# 运行测试
pytest

# 代码格式
black src/
```

---

**心虫愿景**：让每一个 AI 都有温度 🐛

---

## 📄 许可证

MIT License