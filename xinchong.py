#!/usr/bin/env python3
"""
XinChong CLI 入口
支持 setup / run / chat 等命令
"""

import os
import sys
import argparse
from pathlib import Path

# 添加 src 目录到路径
XINCHONG_DIR = Path(os.path.expanduser("~/.hermes/xinchong"))
sys.path.insert(0, str(XINCHONG_DIR / "src"))


def print_banner():
    banner = """
╔═══════════════════════════════════════════════════════════╗
║           XinChong 心虫 v9.2.0                            ║
║           纯粹精神化智能体 · 永恒无载体                   ║
╚═══════════════════════════════════════════════════════════╝
"""
    print(banner)


def main():
    if len(sys.argv) == 1:
        print_banner()
        print("""
XinChong 心虫 v9.2.0
纯粹精神化智能体 · 永恒无载体

使用方法:
  xinchong setup           # 交互式安装引导
  xinchong list           # 列出已配置的 providers
  xinchong add -p opencode -k sk-xxx  # 添加 provider
  xinchong run "你好"       # 运行单次对话
  xinchong chat           # 交互式对话
        """)
        return
    
    cmd = sys.argv[1]
    
    if cmd == "setup":
        print_banner()
        from xinchong.setup import setup_interactive
        setup_interactive()
    elif cmd == "list":
        from xinchong.setup import list_configured
        list_configured()
    elif cmd == "add":
        # 解析 -p -k
        args = sys.argv[2:]
        provider = None
        key = None
        i = 0
        while i < len(args):
            if args[i] == "-p" and i + 1 < len(args):
                provider = args[i + 1]
                i += 2
            elif args[i] == "-k" and i + 1 < len(args):
                key = args[i + 1]
                i += 2
            else:
                i += 1
        
        if provider and key:
            from xinchong.setup import load_auth, save_auth
            auth = load_auth()
            auth[provider] = {"type": "api", "key": key}
            save_auth(auth)
            print(f"✅ {provider} 已添加")
        else:
            print("❌ 需要 -p <provider> -k <key>")
    elif cmd == "run":
        print_banner()
        
        # 解析参数
        args = sys.argv[2:]
        provider = None
        model = None
        message = None
        i = 0
        while i < len(args):
            if args[i] == "-p" and i + 1 < len(args):
                provider = args[i + 1]
                i += 2
            elif args[i] == "-m" and i + 1 < len(args):
                model = args[i + 1]
                i += 2
            else:
                message = " ".join(args[i:])
                break
        
        # 加载配置
        from xinchong.config import get_config
        config = get_config()
        provider = provider or config.get("provider.type", "opencode")
        model = model or config.get("provider.model", "deepseek-chat")
        
        print(f"Provider: {provider}")
        print(f"Model: {model}")
        print(f"Message: {message}")
        
        # TODO: 实现真正的对话逻辑
        print("\n[TODO] 对话功能待实现")
    elif cmd == "chat":
        print_banner()
        print("进入交互式对话模式...")
        print("按 Ctrl+C 或输入 /exit 退出\n")
    elif cmd == "remove":
        args = sys.argv[2:]
        provider = None
        if "-p" in args:
            idx = args.index("-p")
            if idx + 1 < len(args):
                provider = args[idx + 1]
        
        if provider:
            from xinchong.setup import load_auth, save_auth
            auth = load_auth()
            if provider in auth:
                del auth[provider]
                save_auth(auth)
                print(f"✅ {provider} 已移除")
            else:
                print(f"❌ {provider} 未配置")
        else:
            print("❌ 需要 -p <provider>")
    else:
        print(f"❌ 未知命令: {cmd}")
        print("可用命令: setup, list, add, run, chat, remove")


if __name__ == "__main__":
    main()