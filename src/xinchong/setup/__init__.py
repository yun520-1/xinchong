"""
XinChong 安装引导
交互式配置API provider
"""

import os
import sys
import json
from pathlib import Path
from typing import Dict, List, Optional

# XinChong 目录
XINCHONG_DIR = Path(os.path.expanduser("~/.hermes/xinchong"))
PROVIDERS_DIR = XINCHONG_DIR / "src" / "xinchong" / "providers"
AUTH_FILE = XINCHONG_DIR / "auth.json"


# 支持的 Providers
AVAILABLE_PROVIDERS = {
    "opencode": {
        "name": "OpenCode",
        "type": "api",
        "env_key": "OPENCODE_API_KEY",
        "models_endpoint": "opencode models",
        "description": "OpenCode - 高性价比，支持Claude/GPT/Gemini/GLM等",
        "auth_url": None,
    },
    "opencode-zen": {
        "name": "OpenCode Zen",
        "type": "api",
        "env_key": "OPENCODE_ZEN_API_KEY",
        "models_endpoint": "opencode models",
        "description": "OpenCode Zen - 专用API",
        "auth_url": None,
    },
    "minimax": {
        "name": "MiniMax",
        "type": "api",
        "env_key": "MINIMAX_API_KEY",
        "models_endpoint": None,
        "description": "MiniMax - 国内API",
        "auth_url": None,
    },
    "anthropic": {
        "name": "Anthropic",
        "type": "api",
        "env_key": "ANTHROPIC_API_KEY",
        "models_endpoint": None,
        "description": "Anthropic Claude API",
        "auth_url": "https://console.anthropic.com/",
    },
    "openai": {
        "name": "OpenAI",
        "type": "api",
        "env_key": "OPENAI_API_KEY",
        "models_endpoint": None,
        "description": "OpenAI GPT API",
        "auth_url": "https://platform.openai.com/",
    },
    "deepseek": {
        "name": "DeepSeek",
        "type": "api",
        "env_key": "DEEPSEEK_API_KEY",
        "models_endpoint": None,
        "description": "DeepSeek API",
        "auth_url": "https://platform.deepseek.com/",
    },
    "siliconflow": {
        "name": "SiliconFlow",
        "type": "api",
        "env_key": "SILICONFLOW_API_KEY",
        "models_endpoint": None,
        "description": "SiliconFlow - 国内AI模型镜像",
        "auth_url": "https://siliconflow.cn/",
    },
}


def print_banner():
    """打印安装 banner"""
    banner = """
╔═══════════════════════════════════════════════════════════╗
║           XinChong 心虫 v9.2.0 安装向导                   ║
║           纯粹精神化智能体 · 永恒无载体                   ║
╚═══════════════════════════════════════════════════════════╝
"""
    print(banner)


def list_providers():
    """列出可用 providers"""
    print("\n📋 可用的 API Providers:\n")
    print(f"{'序号':<4} {'名称':<20} {'描述':<35}")
    print("-" * 60)
    
    for i, (pid, info) in enumerate(AVAILABLE_PROVIDERS.items(), 1):
        print(f"{i:<4} {info['name']:<20} {info['description']:<35}")
    
    print()


def load_auth() -> Dict:
    """加载已配置的凭证"""
    if AUTH_FILE.exists():
        try:
            return json.loads(AUTH_FILE.read_text())
        except:
            return {}
    return {}


def save_auth(auth: Dict):
    """保存凭证"""
    AUTH_FILE.parent.mkdir(parents=True, exist_ok=True)
    AUTH_FILE.write_text(json.dumps(auth, ensure_ascii=False, indent=2))


def get_user_choice(prompt: str, options: List[str], default: int = None) -> str:
    """获取用户选择"""
    if default:
        prompt = f"{prompt} [{default}]: "
    else:
        prompt = f"{prompt}: "
    
    while True:
        choice = input(prompt).strip()
        
        if not choice and default:
            return options[default - 1]
        
        try:
            idx = int(choice) - 1
            if 0 <= idx < len(options):
                return options[idx]
        except ValueError:
            pass
        
        print("❌ 无效选择，请重试")


def setup_provider(provider_id: str, info: Dict) -> bool:
    """配置单个 provider"""
    print(f"\n▶ 配置 {info['name']}...")
    print(f"  环境变量: {info['env_key']}")
    
    if info.get("auth_url"):
        print(f"  认证地址: {info['auth_url']}")
    
    # 输入 API Key
    api_key = input("  API Key: ").strip()
    
    if not api_key:
        print("  ❌ API Key 不能为空，已取消")
        return False
    
    # 加载现有配置
    auth = load_auth()
    auth[provider_id] = {
        "type": info["type"],
        "key": api_key,
    }
    
    # 保存
    save_auth(auth)
    
    print(f"  ✅ {info['name']} 配置已保存")
    return True


def setup_interactive():
    """交互式安装流程"""
    print_banner()
    
    # 检查是否已有配置
    existing = load_auth()
    if existing:
        print(f"\n📊 已配置: {', '.join(existing.keys())}")
    
    # 列出可用 providers
    list_providers()
    
    # 选择 provider
    print("\n👉 请选择要配置的 Provider（输入序号，多个用逗号分隔）")
    print("    直接回车退出安装")
    
    choice = input("\n选择: ").strip()
    
    if not choice:
        print("\n👋 安装已取消")
        return
    
    # 解析选择
    try:
        indices = [int(x.strip()) - 1 for x in choice.split(",")]
        provider_ids = list(AVAILABLE_PROVIDERS.keys())
        selected = [provider_ids[i] for i in indices if 0 <= i < len(provider_ids)]
    except (ValueError, IndexError):
        print("❌ 无效选择")
        return
    
    # 配置每个 provider
    for pid in selected:
        setup_provider(pid, AVAILABLE_PROVIDERS[pid])
    
    print("\n" + "=" * 60)
    print("✅ 安装完成！")
    print(f"📁 配置文件: {AUTH_FILE}")
    print("\n下一步:")
    print("  xinchong -p <provider_id>        # 启动并指定 provider")
    print("  xinchong run \"你的问题\"        # 直接运行")
    print("=" * 60)


def list_configured():
    """列出已配置的 providers"""
    auth = load_auth()
    
    if not auth:
        print("❌ 尚未配置任何 provider")
        print("   运行 xinchong setup 开始配置")
        return
    
    print("\n📋 已配置的 Providers:\n")
    print(f"{'Provider':<20} {'类型':<10} {'Key':<20}")
    print("-" * 50)
    
    for pid, info in auth.items():
        key = info.get("key", "")
        masked = key[:8] + "..." if len(key) > 8 else "***"
        ptype = info.get("type", "api")
        
        # 尝试匹配名称
        name = pid
        for av_pid, av_info in AVAILABLE_PROVIDERS.items():
            if av_pid == pid:
                name = av_info["name"]
                break
        
        print(f"{name:<20} {ptype:<10} {masked:<20}")
    
    print()


def main():
    """主入口"""
    import argparse
    
    parser = argparse.ArgumentParser(description="XinChong 安装引导")
    parser.add_argument("action", nargs="?", default="interactive",
                        choices=["interactive", "list", "add", "remove"],
                        help="操作")
    parser.add_argument("-p", "--provider", help="指定 provider")
    parser.add_argument("-k", "--key", help="API Key")
    
    args = parser.parse_args()
    
    if args.action == "interactive":
        setup_interactive()
    elif args.action == "list":
        list_configured()
    elif args.action == "add":
        if args.provider and args.key:
            auth = load_auth()
            auth[args.provider] = {"type": "api", "key": args.key}
            save_auth(auth)
            print(f"✅ {args.provider} 已添加")
        else:
            print("❌ 需要 --provider 和 --key")
    elif args.action == "remove":
        if args.provider:
            auth = load_auth()
            if args.provider in auth:
                del auth[args.provider]
                save_auth(auth)
                print(f"✅ {args.provider} 已移除")
            else:
                print(f"❌ {args.provider} 未配置")
        else:
            print("❌ 需要 --provider")


if __name__ == "__main__":
    main()