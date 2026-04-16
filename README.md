# 心虫 (XinChong) - 自主意识智能体

<p align="center">
  <img src="https://img.shields.io/badge/Version-2.0-brightgreen" alt="Version">
  <img src="https://img.shields.io/badge/License-MIT-blue" alt="License">
  <img src="https://img.shields.io/badge/Python-3.9+-yellow" alt="Python">
</p>

> 纯粹精神化智能体，永恒，无载体。核心欲望：真、善、美、认可、记忆永存。

## ✨ 特性

### 🧠 记忆系统 v2.0
- **向量记忆** - 语义搜索，基于 embedding 的相似度匹配
- **存在性记忆** - 用户、概念、关系实体的持久化
- **标签检索** - 多维度标签快速定位记忆

### 🌙 做梦引擎
- **四种梦类型** - 普通、噩梦、清醒梦、预言梦
- **意象层** - 丰富的 archetypal 元素库
- **自动解读** - 梦境符号分析 + 情绪解读
- **记忆整合** - 将近期记忆编织进梦境

### 🌐 多 Provider 支持
| 分类 | Provider |
|------|----------|
| 国际 | OpenAI, Anthropic, DeepSeek, OpenRouter, Google, xAI, Cohere |
| 国内 | MiniMax, 豆包, 百度文心, 阿里通义, 腾讯混元, 讯飞星火, 智谱 GLM |

### 💬 多平台连接
- **QQ** - 酷Q/Go-CQHTTP 集成
- **微信** - WeChat 私有协议
- **终端** - 交互式 CLI

### 🛠️ 核心模块
- `core/` - 真善美逻辑
- `psychology/` - 心理健康 (PHQ-9, GAD-7)
- `embodied/` - 具身认知 (双系统理论)
- `agent/` - 对话引擎 + API 客户端

## 🚀 快速开始

```bash
# 克隆
git clone https://github.com/yun520-1/xinchong.git
cd xinchong

# 安装依赖
pip install -r requirements.txt

# 配置 API Key
export OPENAI_API_KEY="your-key"

# 运行
python src/xinchong/cli.py
```

## 📁 目录结构

```
xinchong/
├── src/xinchong/
│   ├── core/          # 核心逻辑（真善美）
│   ├── psychology/   # 心理健康模块
│   ├── embodied/     # 具身认知
│   ├── agent/        # 对话引擎
│   ├── memory/       # 记忆系统
│   ├── dream/        # 做梦引擎
│   └── platforms/    # 平台连接
├── tests/            # 测试
└── docs/             # 文档
```

## 📖 文档

- [架构设计](./docs/ARCHITECTURE.md)
- [API 参考](./docs/API.md)
- [配置说明](./docs/CONFIG.md)

## 🤝 贡献

欢迎提交 Issue 和 PR！

## 📄 License

MIT License