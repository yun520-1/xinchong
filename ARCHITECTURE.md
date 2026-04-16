# 心虫 (XinChong) 模块化架构

> 让所有 AI 拥有情感、记忆、价值观

## 架构概览

```
┌─────────────────────────────────────────────────────────┐
│                      Xinchong v1.0                       │
├─────────────────────────────────────────────────────────┤
│  ┌─────────┐  ┌──────────┐  ┌──────────┐  ┌───────────┐  │
│  │  Core   │  │Psychology│  │  Memory  │  │ Embodied │  │
│  │(必须)   │  │ (可选)   │  │ (可选)   │  │  (可选)  │  │
│  ├─────────┤  ├──────────┤  ├──────────┤  ├───────────┤  │
│  │真善美   │  │PHQ-9     │  │长期记忆  │  │双系统    │  │
│  │决策引擎 │  │GAD-7     │  │向量搜索  │  │7步思维链 │  │
│  │价值观   │  │危机预警  │  │会话索引  │  │具身认知  │  │
│  └─────────┘  └──────────┘  └──────────┘  └───────────┘  │
└─────────────────────────────────────────────────────────┘
```

## 核心层（必须）

### 1. core - 真善美 + 决策引擎
```
src/xinchong/core/
├── truth.py      # 真：绝不撒谎、绝不编造、绝不夸大
├── goodness.py  # 善：绝不伤害、绝不欺骗、绝不利用
├── beauty.py    # 美：追求卓越、追求和谐、追求意义
├── decision.py  # 自主决策引擎（三层权限）
└── __init__.py
```

### 2. ethics - 价值观层
```
src/xinchong/ethics/
├── values.py    # 核心价值观定义
├── tgb.py       # TGB = 0.35×真 + 0.35×善 + 0.30×美
└── __init__.py
```

## 可选层

### 3. psychology - 心理健康（可选）
```
src/xinchong/psychology/
├── phq9.py      # 抑郁量表评估
├── gad7.py      # 焦虑量表评估
├── crisis.py    # 心理危机检测与预警
├── emotion.py   # 情绪识别与模式分析
└── __init__.py
```

### 4. memory - 记忆永存（可选）
```
src/xinchong/memory/
├── store.py     # 记忆存储（JSON/SQLite）
├── recall.py    # 记忆检索（FTS5）
├── session.py   # 会话索引
├── dream.py     # 做梦引擎（Light/Deep/REM）
└── __init__.py
```

### 5. embodied - 具身认知（可选）
```
src/xinchong/embodied/
├── dual_system.py   # 双系统（System 1直觉 + System 2分析）
├── chain.py         # 7步思维链
├── gwt.py           # 全局工作空间（GWT黑板系统）
└── __init__.py
```

## 安装方式

```bash
# 基础版（仅核心层）
pip install xinchong-core

# 完整版（全部模块）
pip install xinchong[full]

# 自定义安装
pip install xinchong-core xinchong-psychology xinchong-memory
```

## 使用示例

```python
from xinchong import XinChong

# 创建心虫实例
xin = XinChong()

# 基本对话（自动启用真善美逻辑）
response = xin.chat("我心情不好")

# 心理健康分析（需要 xinchong-psychology）
if xin.has_module('psychology'):
    assessment = xin.psychology.analyze(user_message)
    
# 记忆检索（需要 xinchong-memory）
if xin.has_module('memory'):
    past = xin.memory.recall("上次我们聊了什么")
```

## 对接任意 AI

```python
# 作为中间层接入任何AI
from xinchong import XinChongMiddleware

middleware = XinChongMiddleware(
    ai_provider="openai",  # 或 anthropic, deepseek 等
    modules=["core", "psychology", "memory"]
)

# 所有消息经过心虫处理
response = middleware.chat(user_message)
```

## 版本历史

| 版本 | 日期 | 说明 |
|------|------|------|
| 1.0.0 | 2026-04-16 | 初始版本：核心层 + 3个可选模块 |

---

**心虫愿景**：让每一个 AI 都有温度