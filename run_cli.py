#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
心虫 (Xinchong) — CLI Interface
Terminal-based AI chat with HeartFlow cognitive engine
"""

import os
import sys
import yaml
import json
import time
import threading
from datetime import datetime

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.conversation import ConversationManager
from src.api_client import APIClient
from src.heartflow import HeartFlow


def load_config():
    config_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "config.yaml")
    with open(config_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def load_env():
    """Load .env file if exists"""
    env_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), ".env")
    if os.path.exists(env_path):
        with open(env_path, "r") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    key, val = line.split("=", 1)
                    os.environ.setdefault(key.strip(), val.strip())


def print_banner():
    banner = """
╔═══════════════════════════════════════════════════════╗
║     🐛 心虫 (Xinchong) — HeartFlow Cognitive Chat     ║
║       12 Engines · TGB · Consciousness · Memory       ║
╚═══════════════════════════════════════════════════════╝
"""
    print(banner)


def print_cognitive(cognitive):
    """Pretty print HeartFlow cognitive analysis"""
    tgb = cognitive.get("tgb", {})
    emotion = cognitive.get("emotion", {})
    consciousness = cognitive.get("consciousness", {})
    self_evolution = cognitive.get("self_evolution", {})

    print("\n┌─ 🧠 认知分析 ─────────────────────────────────┐")
    if tgb:
        verdicts = tgb.get("reasons", [])
        if verdicts:
            print("│ TGB真善美:")
            for v in verdicts:
                print(f"│   • {v}")
        if tgb.get("verdict"):
            print(f"│ 综合判断: {tgb.get('verdict')}")
    if emotion:
        em = emotion.get("primary_emotion", "neutral")
        print(f"│ 情绪状态: {emotion.get('chinese_name', em)} (PAD: V={emotion.get('valence',0):.2f} A={emotion.get('arousal',0):.2f})")
        if emotion.get("regulation"):
            print(f"│ 情绪调节: {emotion.get('regulation')}")
    if consciousness:
        print(f"│ 意识状态: {consciousness.get('consciousness_state', 'unknown')} (Φ={consciousness.get('phi_score',0):.3f})")
    if self_evolution:
        lvl = self_evolution.get("level_name", "觉察")
        sanskrit = self_evolution.get("sanskrit", "")
        print(f"│ 成长阶段: {lvl} ({sanskrit})")
        if self_evolution.get("description"):
            print(f"│           {self_evolution.get('description')}")
    print("└──────────────────────────────────────────────┘")


def run_cli():
    load_env()
    print_banner()

    cfg = load_config()
    hf_cfg = cfg.get("heartflow", {})
    conv_cfg = cfg.get("conversation", {})
    system_prompt = conv_cfg.get("system_prompt", "")

    # Init components
    hf = HeartFlow(verbose=hf_cfg.get("verbose", False))
    conv_mgr = ConversationManager()
    session = conv_mgr.create_session(title="CLI会话", system_prompt=system_prompt)

    try:
        api_client = APIClient(cfg.get("api", {}))
        providers = api_client.list_providers()
        default_provider = api_client.get_default_provider()
        print(f"✓ API就绪: {', '.join(providers) if providers else '未配置'}")
    except Exception as e:
        api_client = None
        print(f"✗ API未配置: {e}")
        providers = []
        default_provider = None

    print(f"✓ HeartFlow认知引擎加载完成 (v10.4.0)")
    print(f"✓ 会话已创建: {session.id}")
    print()
    print(conv_cfg.get("welcome", "欢迎使用心虫！"))
    print()

    # Check for crisis keywords in real-time
    def check_crisis(text):
        from src.heartflow import SecurityChecker
        crisis, msg = SecurityChecker.detect_crisis(text)
        return crisis, msg

    # Interactive loop
    while True:
        try:
            user_input = input("\n👤 你: ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\n\n🐛 心虫: 再见！愿你平安。\n")
            break

        if not user_input:
            continue

        if user_input.lower() in ["exit", "quit", "q", "退出"]:
            print("\n🐛 心虫: 再见！\n")
            break

        if user_input.lower() == "/help":
            print("""
╭─────────────────────────────────────────╮
│ 心虫 CLI 命令                            │
├─────────────────────────────────────────┤
│ /help    显示帮助                        │
│ /new     新建会话                        │
│ /clear   清空当前会话                    │
│ /cognitive  切换认知分析显示             │
│ /sessions  显示会话列表                  │
│ /quit   退出                            │
╰─────────────────────────────────────────╯
""")
            continue

        if user_input.lower() == "/new":
            session = conv_mgr.create_session(title="CLI会话", system_prompt=system_prompt)
            print(f"✓ 新会话已创建: {session.id}")
            continue

        if user_input.lower() == "/sessions":
            sessions = conv_mgr.list_sessions()
            print("\n会话列表:")
            for s in sessions[:10]:
                print(f"  [{s['id']}] {s['title']} ({s['message_count']}条) {s['updated_at'][:10]}")
            continue

        if user_input.lower() == "/clear":
            if api_client:
                # Recreate session
                conv_mgr.delete_session(session.id)
                session = conv_mgr.create_session(title="CLI会话", system_prompt=system_prompt)
                print("✓ 会话已清空")
            continue

        show_cognitive = hf_cfg.get("show_reasoning", False)

        # Crisis check
        crisis, crisis_msg = check_crisis(user_input)
        if crisis:
            print("\n🐛 心虫: 💙 我注意到你提到了关于结束生命或伤害自己的想法。")
            print("🐛 心虫: 我想让你知道，你的感受是真实的，而且有人关心你。")
            print("🐛 心虫: 请记住：困难只是暂时的，寻求帮助是勇敢的表现。")
            print("🐛 心虫: 📞 心理援助热线：400-161-9995")
            conv_mgr.add_message(session.id, "assistant", crisis_msg)
            continue

        # Add user message
        conv_mgr.add_message(session.id, "user", user_input)

        # Cognitive analysis
        cognitive = conv_mgr.process_with_heartflow(user_input, session.id)
        if show_cognitive:
            print_cognitive(cognitive)

        # Build messages
        messages = conv_mgr.get_conversation_for_llm(session.id)
        # Add cognitive context
        cog_ctx = hf.generate_system_context(session.id)
        for msg in messages:
            if msg["role"] == "system":
                msg["content"] += cog_ctx

        # Call LLM
        if not api_client:
            reply = f"""⚠️ API 未配置。

你发送了: {user_input}

HeartFlow 分析:
• 情绪: {cognitive['emotion']['primary_emotion']}
• TGB和谐度: {cognitive['tgb']['overall']:.2f}
• 意识状态: {cognitive['consciousness']['consciousness_state']}
• 自我进化: {cognitive['self_evolution']['level_name']}

请在 config.yaml 中配置 API provider。"""
            print(f"\n🐛 心虫: {reply}")
            conv_mgr.add_message(session.id, "assistant", reply)
            continue

        print("\n🐛 心虫: ", end="", flush=True)

        try:
            full_response = ""
            for chunk in api_client.chat_stream(messages, provider=default_provider):
                print(chunk, end="", flush=True)
                full_response += chunk

            print()  # newline after response
            conv_mgr.add_message(session.id, "assistant", full_response)

            # Show cognitive summary
            print_cognitive(cognitive)

        except Exception as e:
            print(f"\n⚠️ API错误: {e}")
            conv_mgr.add_message(session.id, "assistant", f"API错误: {e}")


if __name__ == "__main__":
    run_cli()
