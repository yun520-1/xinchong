# 心虫 (Xinchong)

> 🐛 An independent AI chat application powered by HeartFlow cognitive engine

## Features

- **12 Cognitive Engines**: Decision, Emotion, Consciousness, TGB Ethics, Mental Health, etc.
- **Multi-API Support**: OpenAI, Anthropic, OpenRouter, Ollama, Gemini
- **TGB Dialectics**: Truth-Goodness-Beauty ethical synthesis
- **Mental Health Guardian**: PHQ-9/GAD-7 crisis detection
- **Persistent Memory**: Multi-session conversation memory
- **Web + CLI Interface**: Both web UI and terminal chat

## Quick Start

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Configure API keys
cp .en2.0.0example .env
# Edit .env with your API keys

# 3. Run Web UI
python run_web.py
# Open http://localhost:8765

# Or run CLI
python run_cli.py
```

## Configuration

Edit `config.yaml` to configure:
- Default API provider
- System prompt
- HeartFlow settings
- Memory limits

## Architecture

```
xinchong/
├── config.yaml          # Configuration
├── run_web.py          # Web server entry
├── run_cli.py          # CLI entry
├── src/
│   ├── heartflow.py     # 12-engine cognitive core
│   ├── api_client.py    # Multi-provider API abstraction
│   ├── conversation.py   # Session & memory management
│   └── web/
│       ├── app.py       # Flask application
│       └── templates/
│           └── index.html
└── data/
    └── sessions/         # Persistent session storage
```

## HeartFlow Engines

| # | Engine | Description |
|---|--------|-------------|
| 1 | DecisionEngine | Multi-framework ethical decisions |
| 2 | LogicModelEngine | Toulmin argument analysis |
| 3 | ArchetypeEngine | Jungian personality archetypes |
| 4 | MentalHealthEngine | PHQ-9 + GAD-7 + crisis detection |
| 5 | EmotionEngine | PAD emotion model |
| 6 | SomaticMemoryEngine | Body-state memory |
| 7 | ConsciousnessEngine | IIT Φ + GWT consciousness |
| 8 | TGBEngine | Truth-Goodness-Beauty synthesis |
| 9 | SelfLevelEngine | Six-layer growth practice |
| 10 | EntropyEngine | Information ordering |
| 11 | WangDongyueEngine | 递弱代偿 existential analysis |
| 12 | SecurityChecker | Input validation + crisis guard |

---

MIT License — 致敬 HeartFlow 团队
