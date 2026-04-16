"""
XinChong 对话模块
调用各服务商 API 进行对话
"""

import os
import sys
import json
import subprocess
from pathlib import Path
from typing import Dict, Optional, List

# 目录
XINCHONG_DIR = Path(os.path.expanduser("~/.hermes/xinchong"))
AUTH_FILE = XINCHONG_DIR / "auth.json"


def load_auth() -> Dict:
    """加载凭证"""
    if AUTH_FILE.exists():
        try:
            return json.loads(AUTH_FILE.read_text())
        except:
            return {}
    return {}


def list_providers() -> Dict:
    """获取已配置的 providers"""
    return load_auth()


def list_models(provider: str = None) -> List[str]:
    """获取可用模型列表"""
    result = subprocess.run(
        ["opencode", "models"],
        capture_output=True,
        text=True,
        timeout=30
    )
    
    if result.returncode != 0:
        return []
    
    lines = result.stdout.strip().split("\n")
    models = []
    
    # 过滤 provider
    prefix = f"{provider}/" if provider else None
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
        if line.startswith("opencode/"):
            continue
        if prefix:
            if line.startswith(prefix):
                models.append(line.replace(prefix, ""))
        else:
            # 列出所有，去掉 provider/ 前缀
            if "/" in line:
                p, m = line.split("/", 1)
                models.append(m)
            else:
                models.append(line)
    
    return list(set(models))  # 去重


def call_opencode(message: str, provider: str = "opencode", model: str = None) -> str:
    """调用 opencode 执行对话"""
    cmd = ["opencode", "run", "-m", f"{provider}/{model}"] if model else ["opencode", "run"]
    cmd.append(message)
    
    result = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        timeout=120
    )
    
    if result.returncode != 0:
        return f"❌ 调用失败: {result.stderr}"
    
    return result.stdout


def call_custom_api(message: str, api_url: str, api_key: str, model: str = "deepseek-chat") -> str:
    """调用自定义 API"""
    import requests
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": model,
        "messages": [
            {"role": "user", "content": message}
        ],
        "max_tokens": 4096
    }
    
    try:
        resp = requests.post(
            f"{api_url.rstrip('/')}/v1/chat/completions",
            headers=headers,
            json=payload,
            timeout=120
        )
        
        if resp.status_code != 200:
            return f"❌ API 错误 {resp.status_code}: {resp.text}"
        
        data = resp.json()
        return data.get("choices", [{}])[0].get("message", {}).get("content", "")
    
    except Exception as e:
        return f"❌ 调用失败: {e}"


def chat_loop(provider: str = None, model: str = None):
    """交互式对话循环"""
    print_banner()
    print(f"Provider: {provider or 'opencode'}")
    print(f"Model: {model or '默认'}")
    print("\n输入消息进行对话，输入 /exit 退出")
    print("使用 /m <model> 切换模型，输入 /p <provider> 切���服务商\n")
    
    current_provider = provider or "opencode"
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
                models = list_models(current_provider)
                print(f"\n📋 可用模型 ({current_provider}):")
                for m in models[:20]:
                    print(f"  - {m}")
                if len(models) > 20:
                    print(f"  ... 还有 {len(models)-20} 个")
                continue
            
            # 列出服务商
            if user_input == "/providers":
                providers = list_providers()
                print("\n📋 已配置的服务商:")
                for p in providers:
                    print(f"  - {p}")
                continue
            
            # 对话
            print(f"\n🤖 心虫: ", end="", flush=True)
            
            if current_provider == "opencode":
                response = call_opencode(user_input, "opencode", current_model)
                print(response)
            else:
                # 自定义 API
                auth = load_auth()
                if current_provider in auth:
                    config = auth[current_provider]
                    response = call_custom_api(
                        user_input,
                        config.get("url", "https://api.openai.com"),
                        config.get("key", ""),
                        current_model
                    )
                    print(response)
                else:
                    print(f"❌ 服务商 {current_provider} 未配置")
            
        except KeyboardInterrupt:
            print("\n👋 再见")
            break
        except Exception as e:
            print(f"❌ 错误: {e}")


def print_banner():
    banner = """
╔═══════════════════════════════════════════════════════════╗
║           XinChong 心虫 v9.2.0                            ║
║           纯粹精神化智能体 · 永恒无载体                   ║
╚═══════════════════════════════════════════════════════════╝
"""
    print(banner)


# 主入口
if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="XinChong 对话")
    parser.add_argument("-p", "--provider", default="opencode", help="服务商")
    parser.add_argument("-m", "--model", help="模型")
    parser.add_argument("message", nargs="?", help="消息")
    parser.add_argument("--list-models", action="store_true", help="列出模型")
    
    args = parser.parse_args()
    
    if args.list_models:
        models = list_models(args.provider)
        print(f"\n📋 可用模型 ({args.provider}):")
        for m in models:
            print(f"  - {m}")
    elif args.message:
        # 单次对话
        print_banner()
        response = call_opencode(args.message, args.provider, args.model)
        print(response)
    else:
        # 交互模式
        chat_loop(args.provider, args.model)