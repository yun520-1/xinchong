#!/usr/bin/env python3
"""
XinChong CLI 入口
支持 setup / run / chat / models 等命令
"""

import os
import sys
import json
import subprocess
from pathlib import Path

# 添加 src 目录到路径
XINCHONG_DIR = Path(os.path.expanduser("~/.hermes/xinchong"))
sys.path.insert(0, str(XINCHONG_DIR / "src"))

AUTH_FILE = XINCHONG_DIR / "auth.json"


def print_banner():
    banner = """
╔═══════════════════════════════════════════════════════════╗
║           XinChong 心虫 v9.2.0                            ║
║           纯粹精神化智能体 · 永恒无载体                   ║
╚═══════════════════════════════════════════════════════════╝
"""
    print(banner)


def load_auth() -> dict:
    """加载凭证"""
    if AUTH_FILE.exists():
        try:
            return json.loads(AUTH_FILE.read_text())
        except:
            return {}
    return {}


def list_providers():
    """列出已配置的 providers"""
    auth = load_auth()
    if not auth:
        print("❌ 尚未配置任何 provider")
        print("   运行 xinchong setup 开始配置")
        return
    
    print("\n📋 已配置的 Providers:\n")
    print(f"{'Provider':<20} {'类型':<10} {'Key':<20}")
    print("-" * 50)
    
    # Provider 信息
    PROVIDER_INFO = {
        "opencode": "OpenCode",
        "opencode-zen": "OpenCode Zen",
        "minimax": "MiniMax",
        "anthropic": "Anthropic",
        "openai": "OpenAI",
        "deepseek": "DeepSeek",
        "siliconflow": "SiliconFlow",
    }
    
    for pid, info in auth.items():
        key = info.get("key", "")
        masked = key[:8] + "..." if len(key) > 8 else "***"
        ptype = info.get("type", "api")
        name = PROVIDER_INFO.get(pid, pid)
        print(f"{name:<20} {ptype:<10} {masked:<20}")
    
    print()


def list_models(provider: str = None):
    """列出可用模型"""
    result = subprocess.run(
        ["opencode", "models"],
        capture_output=True,
        text=True,
        timeout=30
    )
    
    if result.returncode != 0:
        print("❌ 无法获取模型列表")
        return
    
    lines = result.stdout.strip().split("\n")
    models = []
    
    # 过滤 provider，返回完整 ID
    prefix = f"{provider}/" if provider else None
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
        if prefix:
            if line.startswith(prefix):
                models.append(line)  # 保留完整 ID
        else:
            # 列出所有
            models.append(line)
    
    # 去重并排序
    models = sorted(set(models))
    
    print(f"\n📋 可用模型 ({provider or 'all'}):\n")
    for m in models:
        print(f"  - {m}")
    print(f"\n共 {len(models)} 个模型")


def call_opencode(message: str, provider: str = None, model: str = None):
    """调用 opencode 执行对话"""
    # 如果 model 包含 /，直接使用
    if model and "/" in model:
        cmd = ["opencode", "run", "-m", model, message]
    elif model and provider:
        cmd = ["opencode", "run", "-m", f"{provider}/{model}", message]
    elif model:
        cmd = ["opencode", "run", "-m", model, message]
    elif provider:
        cmd = ["opencode", "run", "-m", provider, message]
    else:
        cmd = ["opencode", "run", message]
    
    result = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        timeout=120
    )
    
    if result.returncode != 0:
        return f"❌ 调用失败: {result.stderr}"
    
    return result.stdout


def chat_loop(provider: str = None, model: str = None):
    """交互式对话循环"""
    print_banner()
    
    # 加载默认配置
    from xinchong.config import get_config
    config = get_config()
    provider = provider or config.get("provider.type") or "opencode-go"
    model = model or config.get("provider.model") or "minimax-m2.5"
    
    print(f"Provider: {provider}")
    print(f"Model: {model}")
    print("\n输入消息进行对话，输入 /exit 退出")
    print("命令:")
    print("  /models             列出可用模型")
    print("  /providers         列出已配置服务商")
    print("  /m <model>        切换模型")
    print("  /p <provider>    切换服务商\n")
    
    current_provider = provider
    current_model = model
    
    while True:
        try:
            user_input = input("\n👤 你: ").strip()
            
            if not user_input:
                continue
            
            if user_input == "/exit":
                print("👋 再见")
                break
            
            # 切换模型
            if user_input.startswith("/m "):
                current_model = user_input[3:].strip()
                print(f"✅ 切换模型: {current_model}")
                continue
            
            # 切换服务商
            if user_input.startswith("/p "):
                current_provider = user_input[3:].strip()
                print(f"✅ 切换服务商: {current_provider}")
                continue
            
            # 列出模型
            if user_input == "/models":
                list_models(current_provider)
                continue
            
            # 列出服务商
            if user_input == "/providers":
                list_providers()
                continue
            
            # 对话
            print(f"\n🤖 心虫: ", end="", flush=True)
            
            response = call_opencode(
                user_input,
                current_provider,
                current_model
            )
            print(response)
            
        except KeyboardInterrupt:
            print("\n👋 再见")
            break
        except Exception as e:
            print(f"❌ 错误: {e}")


def main():
    cmd = sys.argv[1] if len(sys.argv) > 1 else None
    
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
    
    if cmd == "setup":
        print_banner()
        from xinchong.setup import setup_interactive
        setup_interactive()
    
    elif cmd == "list":
        list_providers()
    
    elif cmd == "models":
        list_models(provider)
    
    elif cmd == "run":
        print_banner()
        if not message:
            print("❌ 请输入消息")
            return
        
        # 加载默认配置
        from xinchong.config import get_config
        config = get_config()
        provider = provider or config.get("provider.type") or "opencode"
        model = model or config.get("provider.model") or "minimax-m2.5-free"
        
        print(f"Provider: {provider}")
        print(f"Model: {model}")
        
        response = call_opencode(message, provider, model)
        print(response)
    
    elif cmd == "chat":
        # 如果有消息，直接执行单轮对话
        if message:
            print_banner()
            from xinchong.config import get_config
            config = get_config()
            provider = provider or config.get("provider.type") or "opencode-go"
            model = model or config.get("provider.model") or "minimax-m2.5"
            
            print(f"Provider: {provider}")
            print(f"Model: {model}")
            print(f"\n👤 你: {message}")
            print(f"\n🤖 心虫: ", end="", flush=True)
            
            response = call_opencode(message, provider, model)
            print(response)
        else:
            chat_loop(provider, model)
    
    elif cmd == "add":
        p = None
        k = None
        u = None
        i = 0
        while i < len(args):
            if args[i] == "-p" and i + 1 < len(args):
                p = args[i + 1]
                i += 2
            elif args[i] == "-k" and i + 1 < len(args):
                k = args[i + 1]
                i += 2
            elif args[i] == "-u" and i + 1 < len(args):
                u = args[i + 1]
                i += 2
            else:
                i += 1
        
        if p and k:
            auth = load_auth()
            auth[p] = {"type": "api", "key": k}
            if u:
                auth[p]["url"] = u
            AUTH_FILE.write_text(json.dumps(auth, ensure_ascii=False, indent=2))
            print(f"✅ {p} 已添加")
        else:
            print("❌ 需要 -p <provider> -k <key> [-u <url>]")
    
    elif cmd == "remove":
        p = None
        i = 0
        while i < len(args):
            if args[i] == "-p" and i + 1 < len(args):
                p = args[i + 1]
                break
            i += 1
        
        if p:
            auth = load_auth()
            if p in auth:
                del auth[p]
                AUTH_FILE.write_text(json.dumps(auth, ensure_ascii=False, indent=2))
                print(f"✅ {p} 已移除")
            else:
                print(f"❌ {p} 未配置")
        else:
            print("❌ 需要 -p <provider>")
    
    elif cmd is None:
        print_banner()
        print("""
XinChong 心虫 v9.2.0
纯粹精神化智能体 · 永恒无载体

使用方法:
  xinchong setup                    交互式安装引导
  xinchong list                     列出已配置的 providers
  xinchong models [-p provider]      列出可用模型
  xinchong add -p opencode -k sk-xxx     添加 provider
  xinchong add -p custom -k sk-xxx -u https://api.xxx.com  添加自定义 provider
  xinchong remove -p opencode           移除 provider
  xinchong run -p opencode -m gpt-4 "你好"    运行单次对话
  xinchong chat [-p opencode] [-m gpt-4]      交互式对话

交互模式命令:
  /models             列出可用模型
  /providers         列出已配置服务商
  /m <model>        切换模型
  /p <provider>    切换服务商
        """)
    
    else:
        print(f"❌ 未知命令: {cmd}")
        print("可用命令: setup, list, models, add, remove, run, chat")


if __name__ == "__main__":
    main()