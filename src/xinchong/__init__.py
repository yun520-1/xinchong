#!/usr/bin/env python3
"""
心虫核心模块入口 - 统一启动器
支持通过配置文件指定模块路径
"""

import os
import sys
import json
import importlib.util
from pathlib import Path

# 心虫目录
XINCHONG_DIR = Path(os.path.expanduser("~/.hermes/xinchong"))
CONFIG_DIR = XINCHONG_DIR / "src" / "xinchong" / "config"

def load_config():
    """加载配置"""
    config_path = CONFIG_DIR / "__init__.py"
    if not config_path.exists():
        print(f"配置模块不存在: {config_path}")
        return {}
    
    # 动态加载配置模块
    spec = importlib.util.spec_from_file_location("xinchong_config", config_path)
    config_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(config_module)
    
    return config_module.get_config()

def main():
    """主入口"""
    print("心虫核心模块 v9.2.0")
    print(f"目录: {XINCHONG_DIR}")
    
    # 加载配置
    config = load_config()
    if config:
        print(f"Provider: {config.get('provider.type', 'N/A')}")
        print(f"Model: {config.get('provider.model', 'N/A')}")
    else:
        print("配置加载失败")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())