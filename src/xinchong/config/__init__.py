"""
配置管理
"""

import os
import json
import yaml
from pathlib import Path
from typing import Dict, Any, Optional


# 默认配置
DEFAULT_CONFIG = {
    "provider": {
        "type": "opencode",
        "model": "minimax-m2.5-free",
        "api_key": os.getenv("OPENCODE_ZEN_API_KEY", "")
    },
    "platforms": {
        "weixin": {
            "enabled": False,
            "app_id": os.getenv("WEIXIN_APP_ID", ""),
            "app_secret": os.getenv("WEIXIN_APP_SECRET", "")
        },
        "qq": {
            "enabled": False,
            "app_id": os.getenv("QQ_APP_ID", ""),
            "client_secret": os.getenv("QQ_CLIENT_SECRET", "")
        }
    },
    "memory": {
        "enabled": True,
        "storage_dir": os.path.expanduser("~/.xinchong/memory")
    },
    "psychology": {
        "enabled": True,
        "crisis_intervention": True
    }
}


class Config:
    """配置管理类"""
    
    def __init__(self, config_path: str = None):
        self.config_path = config_path or self._default_config_path()
        self._config = self._load()
    
    def _default_config_path(self) -> str:
        """默认配置文件路径"""
        xinchong_dir = Path(os.path.expanduser("~/.xinchong"))
        return str(xinchong_dir / "config.yaml")
    
    def _load(self) -> Dict[str, Any]:
        """加载配置"""
        config = DEFAULT_CONFIG.copy()
        
        # 如果配置文件存在，读取并合并
        if os.path.exists(self.config_path):
            try:
                with open(self.config_path, encoding="utf-8") as f:
                    user_config = yaml.safe_load(f) or {}
                
                # 深度合并配置
                config = self._merge(config, user_config)
            except Exception as e:
                print(f"加载配置文件失败: {e}")
        
        return config
    
    def _merge(self, default: Dict, user: Dict) -> Dict:
        """合并配置"""
        result = default.copy()
        
        for key, value in user.items():
            if key in result and isinstance(result[key], dict) and isinstance(value, dict):
                result[key] = self._merge(result[key], value)
            else:
                result[key] = value
        
        return result
    
    def get(self, key: str, default: Any = None) -> Any:
        """获取配置值"""
        keys = key.split(".")
        value = self._config
        
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default
        
        return value
    
    def set(self, key: str, value: Any):
        """设置配置值"""
        keys = key.split(".")
        target = self._config
        
        for k in keys[:-1]:
            if k not in target:
                target[k] = {}
            target = target[k]
        
        target[keys[-1]] = value
    
    def save(self):
        """保存配置到文件"""
        os.makedirs(os.path.dirname(self.config_path), exist_ok=True)
        
        with open(self.config_path, "w", encoding="utf-8") as f:
            yaml.dump(self._config, f, allow_unicode=True, default_flow_style=False)
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return self._config.copy()
    
    @property
    def provider(self) -> Dict[str, Any]:
        return self._config.get("provider", {})
    
    @property
    def platforms(self) -> Dict[str, Any]:
        return self._config.get("platforms", {})
    
    @property
    def memory(self) -> Dict[str, Any]:
        return self._config.get("memory", {})
    
    @property
    def psychology(self) -> Dict[str, Any]:
        return self._config.get("psychology", {})


# 全局配置实例
_config = None


def get_config(config_path: str = None) -> Config:
    """获取配置实例"""
    global _config
    if _config is None:
        _config = Config(config_path)
    return _config


def init_config(config_path: str = None, **kwargs) -> Config:
    """初始化配置"""
    global _config
    _config = Config(config_path)
    
    # 设置配置项
    for key, value in kwargs.items():
        _config.set(key, value)
    
    return _config