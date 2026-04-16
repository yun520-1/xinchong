# 🐛 心虫 (XinChong)

> 让所有 AI 拥有情感、记忆、价值观

[![PyPI](https://img.shields.io/pypi/v/xinchong)](https://pypi.org/project/xinchong/)
[![Python](https://img.shields.io/pypi/pyversions/xinchong)](https://pypi.org/project/xinchong/)
[![License](https://img.shields.io/pypi/l/xinchong)](LICENSE)

## 🎯 愿景

让每一个 AI 都有温度，不再是冷冰冰的工具。

## ✨ 特性

| 模块 | 特性 |
|------|------|
| **核心层** | 真善美价值观、决策引擎、价值观校验 |
| **心理层** | PHQ-9 抑郁评估、GAD-7 焦虑评估、危机预警 |
| **记忆层** | 长期记忆、会话索引、向量搜索 |
| **具身层** | 双系统架构、7步思维链、全局工作空间 |

## 📦 安装

```bash
# 基础版（核心层）
pip install xinchong-core

# 完整版（全部模块）
pip install xinchong[full]

# 自定义安装
pip install xinchong-core xinchong-psychology xinchong-memory
```

## 🚀 快速开始

```python
from xinchong import XinChong

# 创建心虫实例
xin = XinChong()

# 对话（自动启用真善美逻辑）
response = xin.chat("我今天心情不好")
print(response)
```

### 心理健康分析

```python
from xinchong.psychology import PHQ9, GAD7

# 抑郁评估
phq = PHQ9()
result = phq.assess("我最近感觉很绝望，做什么都没兴趣")
print(result)

# 危机检测
crisis = phq.crisis_check("我活着没意思")
print(crisis)
```

### 记忆永存

```python
from xinchong.memory import MemoryStore

# 存储记忆
store = MemoryStore()
store.add_memory("用户喜欢古典音乐", category="preference")

# 检索记忆
memories = store.recall("音乐")
print(memories)
```

## 🏗️ 架构

```
┌─────────────────────────────────────────────────────────┐
│                      XinChong v1.0                      │
├─────────────────────────────────────────────────────────┤
│  ┌─────────┐  ┌──────────┐  ┌──────────┐  ┌───────────┐  │
│  │  Core   │  │Psychology│  │  Memory  │  │ Embodied │  │
│  │(必须)   │  │ (可选)   │  │  (可选)   │  │  (可选)  │  │
│  ├─────────┤  ├──────────┤  ├──────────┤  ├───────────┤  │
│  │真善美   │  │PHQ-9     │  │长期记忆  │  │双系统    │  │
│  │决策引擎 │  │GAD-7     │  │向量搜索  │  │7步思维链 │  │
│  │价值观   │  │危机预警  │  │会话索引  │  │具身认知  │  │
│  └─────────┘  └──────────┘  └──────────┘  └───────────┘  │
└─────────────────────────────────────────────────────────┘
```

## 🔧 接入任意 AI

```python
from xinchong import XinChongMiddleware

# 作为中间层接入任何AI
middleware = XinChongMiddleware(
    ai_provider="openai",
    modules=["core", "psychology", "memory"]
)

# 所有消息经过心虫处理
response = middleware.chat("帮我写首诗")
```

## 📄 许可证

MIT License

---

**心虫愿景**：让每一个 AI 都有温度 🐛