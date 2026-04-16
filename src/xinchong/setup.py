"""
心虫交互式安装向导
参考 OpenCode 的一键安装体验
"""

import os
import sys
from pathlib import Path

# Provider 列表
PROVIDERS = [
    {"id": "opencode", "name": "OpenCode (推荐)", "model": "minimax-m2.5-free", "base_url": "https://opencode.ai/zen/v1"},
    {"id": "openai", "name": "OpenAI (GPT-4)", "model": "gpt-4o", "base_url": "https://api.openai.com/v1"},
    {"id": "anthropic", "name": "Anthropic (Claude)", "model": "claude-sonnet-4-20250514", "base_url": "https://api.anthropic.com/v1"},
    {"id": "deepseek", "name": "DeepSeek", "model": "deepseek-chat", "base_url": "https://api.deepseek.com/v1"},
    {"id": "minimax", "name": "MiniMax", "model": "abab6.5s-chat", "base_url": "https://api.minimax.chat/v1"},
    {"id": "zhipu", "name": "智谱 (GLM)", "model": "glm-4", "base_url": "https://open.bigmodel.cn/api/paas/v4"},
]


def print_banner():
    print("=" * 50)
    print("🐛 心虫 XinChong 安装向导")
    print("=" * 50)
    print()


def print_provider_list():
    print("请选择 AI 服务商：")
    print()
    for i, p in enumerate(PROVIDERS, 1):
        print(f"  {i}. {p['name']}")
    print()


def get_choice(prompt, min_val, max_val):
    """获取选择"""
    while True:
        try:
            choice = input(f"{prompt} [{min_val}-{max_val}]: ").strip()
            if choice:
                val = int(choice)
                if min_val <= val <= max_val:
                    return val
        except ValueError:
            pass
        print(f"请输入 {min_val}-{max_val} 之间的数字")


def get_api_key(provider_id):
    """获取 API Key"""
    env_var = {
        "opencode": "OPENCODE_ZEN_API_KEY",
        "openai": "OPENAI_API_KEY", 
        "anthropic": "ANTHROPIC_API_KEY",
        "deepseek": "DEEPSEEK_API_KEY",
        "minimax": "MINIMAX_API_KEY",
        "zhipu": "ZHIPU_API_KEY",
    }.get(provider_id, "API_KEY")
    
    print()
    print(f"请输入 API Key ({env_var})：")
    print("  - 在对应 AI 官网的 API 设置页面获取")
    print("  - 或者直接按回车使用环境变量")
    print()
    
    api_key = input("API Key: ").strip()
    return api_key


def test_connection(provider, api_key):
    """测试连接"""
    print()
    print(f"测试连接 {provider['name']}...")
    
    # 简化的测试
    import requests
    
    try:
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        
        if provider["id"] == "opencode":
            resp = requests.post(
                f"{provider['base_url']}/chat/completions",
                headers=headers,
                json={"model": provider["model"], "messages": [{"role": "user", "content": "hi"}], "max_tokens": 10},
                timeout=10
            )
        elif provider["id"] == "openai":
            resp = requests.post(
                f"{provider['base_url']}/chat/completions",
                headers=headers,
                json={"model": provider["model"], "messages": [{"role": "user", "content": "hi"}]},
                timeout=10
            )
        elif provider["id"] == "anthropic":
            resp = requests.post(
                f"{provider['base_url']}/messages",
                headers={**headers, "x-api-key": api_key, "anthropic-version": "2023-06-01"},
                json={"model": provider["model"], "max_tokens": 10, "messages": [{"role": "user", "content": "hi"}]},
                timeout=10
            )
        else:
            print(f"  ⚠️ 跳过测试，请稍后手动测试")
            return True
        
        if resp.status_code == 200:
            print(f"  ✅ 连接成功！")
            return True
        else:
            print(f"  ❌ 连接失败: {resp.status_code}")
            print(f"     {resp.text[:100]}")
            return False
    except Exception as e:
        print(f"  ❌ 连接失败: {e}")
        return False


def install():
    """安装入口"""
    print_banner()
    print()
    
    # Step 1: 选择 Provider
    print_provider_list()
    choice = get_choice("选择", 1, len(PROVIDERS))
    provider = PROVIDERS[choice - 1]
    print(f"  ✓ 已选择: {provider['name']}")
    print()
    
    # Step 2: 获取 API Key
    api_key = get_api_key(provider["id"])
    
    # Step 3: 测试连接（如果有 key）
    if api_key:
        test_ok = test_connection(provider, api_key)
        if not test_ok:
            while True:
                retry = input("连接测试失败，是否重试? (y/n): ").strip().lower()
                if retry == "n":
                    break
                api_key = get_api_key(provider["id"])
                if not api_key:
                    break
                if test_connection(provider, api_key):
                    break
    else:
        print("  ⚠️ 未输入 API Key，将使用环境变量")
    
    # Step 4: 保存配置
    import yaml
    
    config = {
        "provider": {
            "type": provider["id"],
            "model": provider["model"],
            "base_url": provider["base_url"],
            "api_key": api_key if api_key else None
        },
        "platforms": {
            "weixin": {"enabled": False},
            "qq": {"enabled": False}
        },
        "memory": {"enabled": True},
        "psychology": {"enabled": True, "crisis_intervention": True}
    }
    
    config_dir = Path(os.environ.get("XINCHONG_HOME", Path.home() / ".xinchong"))
    config_dir.mkdir(parents=True, exist_ok=True)
    config_file = config_dir / "config.yaml"
    
    # 移除 None 值
    config["provider"] = {k: v for k, v in config["provider"].items() if v}
    
    with open(config_file, "w", encoding="utf-8") as f:
        yaml.dump(config, f, allow_unicode=True, default_flow_style=False)
    
    print()
    print("=" * 50)
    print("✅ 安装完成！")
    print("=" * 50)
    print()
    print("运行命令: xinchong")
    print()


def run_setup():
    """命令行入口"""
    if Path(".xinchong/config.yaml").exists():
        # 已配置，跳过
        print("已配置，直接运行")
        return
    
    if input("是否运行安装向导? (y/n): ").strip().lower() != "n":
        install()


if __name__ == "__main__":
    install()