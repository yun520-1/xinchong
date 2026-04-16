# Xinchong v2.0 架构

> 集成 OpenClaw + OpenCode + Hermes 的下一代心虫

## 架构概览

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
│  - OpenClaw 记忆系统（向量搜索 + 做梦引擎）                  │
│  - Hermes 平台适配器（QQ + 微信）                           │
└─────────────────────────────────────────────────────────────┘
```

## 模块结构

```
src/xinchong/
├── agent/              # Agent 核心
│   ├── __init__.py     # XinChongAgent 主类
│   ├── api_client.py   # API 客户端（OpenCode 风格）
│   └── conversation.py # 对话管理
│
├── platforms/          # 平台连接（从 Hermes 移植）
│   ├── weixin.py       # 微信
│   ├── qqbot.py        # QQ
│   └── base.py         # 基础适配器
│
├── core/               # 核心模块
│   ├── truth.py        # 真
│   ├── goodness.py     # 善
│   └── beauty.py       # 美
│
├── psychology/         # 心理模块
│   ├── phq9.py         # 抑郁评估
│   ├── gad7.py         # 焦虑评估
│   └── crisis.py       # 危机干预
│
├── memory/             # 记忆系统（从 OpenClaw 提取）
│   ├── store.py        # 记忆存储
│   ├── recall.py       # 记忆检索
│   └── dream.py        # 做梦引擎
│
└── config/             # 配置管理
    ├── __init__.py     # 配置加载
    └── platforms.yaml # 平台配置
```

## 核心特性

### 1. 多平台连接
- **微信**：通过 iLink Bot API 连接
- **QQ**：通过官方 QQ Bot API (v2) 连接
- 其他平台可扩展

### 2. 多 API Provider
- OpenAI
- Anthropic
- DeepSeek
- OpenRouter
- MiniMax
- 更多...

### 3. 真善美价值观
- 每次回复前进行真善美校验
- 心理健康检测（PHQ-9 + GAD-7 + 危机预警）

### 4. 记忆永存
- 长期记忆存储
- 向量搜索
- 做梦引擎（Light/Deep/REM）

### 5. 对话管理
- 多会话支持
- 历史记录保存
- 上下文保持

## 安装方式

```bash
# 克隆仓库
git clone https://github.com/yun520-1/xinchong.git
cd xinchong

# 安装依赖
pip install -e .

# 配置
cp config.example.yaml config.yaml
# 编辑 config.yaml 填写 API Key 和平台配置

# 运行
xinchong run
# 或
python -m xinchong.agent
```

## 配置示例 (config.yaml)

```yaml
# API 配置
provider:
  type: openai          # openai / anthropic / deepseek / openrouter
  model: gpt-4o
  api_key: ${OPENAI_API_KEY}

# 平台配置
platforms:
  weixin:
    enabled: true
    app_id: your_app_id
    app_secret: your_secret
    
  qq:
    enabled: true
    app_id: your_app_id
    client_secret: your_secret

# 记忆配置
memory:
  enabled: true
  storage_dir: ~/.xinchong/memory
  vector_enabled: false

# 心理健康配置
psychology:
  enabled: true
  crisis_intervention: true
```

## 对比 v1.x

| 特性 | v1.x | v2.0 |
|------|------|------|
| 运行方式 | CLI 交互 | CLI + 平台服务 |
| 平台连接 | 无 | QQ + 微信 |
| 记忆系统 | 基础 | 向量 + 做梦 |
| 配置方式 | 环境变量 | YAML 配置文件 |

---

**目标**：比 OpenCode、OpenClaw、Hermes 做得更好，成为下一代 AI Agent 框架