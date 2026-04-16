"""
API 客户端 - 支持多 provider
"""

import os
import json
from typing import Optional, List, Dict


class APIClient:
    """API 客户端，支持多 provider"""
    
    PROVIDERS = ["openai", "anthropic", "deepseek", "openrouter"]
    
    def __init__(self, provider: str = "openai", model: str = None):
        self.provider = provider.lower()
        self.model = model or self._default_model()
        self.api_key = self._get_api_key()
    
    def _default_model(self) -> str:
        defaults = {
            "openai": "gpt-4o",
            "anthropic": "claude-sonnet-4-20250514",
            "deepseek": "deepseek-chat",
            "openrouter": "anthropic/claude-sonnet-4"
        }
        return defaults.get(self.provider, "gpt-4o")
    
    def _get_api_key(self) -> str:
        env_vars = {
            "openai": "OPENAI_API_KEY",
            "anthropic": "ANTHROPIC_API_KEY",
            "deepseek": "DEEPSEEK_API_KEY",
            "openrouter": "OPENROUTER_API_KEY"
        }
        key = os.environ.get(env_vars.get(self.provider, ""))
        if not key:
            raise ValueError(f"Please set {env_vars[self.provider]} environment variable")
        return key
    
    def chat(self, messages: List[Dict], system_prompt: str = None) -> str:
        """发送对话请求"""
        if self.provider == "openai":
            return self._openai_chat(messages, system_prompt)
        elif self.provider == "anthropic":
            return self._anthropic_chat(messages, system_prompt)
        elif self.provider == "deepseek":
            return self._deepseek_chat(messages, system_prompt)
        elif self.provider == "openrouter":
            return self._openrouter_chat(messages, system_prompt)
        else:
            raise ValueError(f"Unsupported provider: {self.provider}")
    
    def _openai_chat(self, messages: List[Dict], system_prompt: str = None) -> str:
        import requests
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        # 合并 system prompt
        if system_prompt:
            full_messages = [{"role": "system", "content": system_prompt}] + messages
        else:
            full_messages = messages
        
        data = {
            "model": self.model,
            "messages": full_messages,
            "temperature": 0.7
        }
        
        response = requests.post(
            "https://api.openai.com/v1/chat/completions",
            headers=headers,
            json=data,
            timeout=60
        )
        
        if response.status_code != 200:
            raise Exception(f"API error: {response.text}")
        
        return response.json()["choices"][0]["message"]["content"]
    
    def _anthropic_chat(self, messages: List[Dict], system_prompt: str = None) -> str:
        import requests
        
        headers = {
            "x-api-key": self.api_key,
            "Content-Type": "application/json",
            "anthropic-version": "2023-06-01"
        }
        
        # 转换消息格式
        claude_messages = []
        if system_prompt:
            claude_messages.append({"role": "user", "content": system_prompt})
        claude_messages.extend(messages)
        
        data = {
            "model": self.model,
            "messages": claude_messages,
            "max_tokens": 4096
        }
        
        response = requests.post(
            "https://api.anthropic.com/v1/messages",
            headers=headers,
            json=data,
            timeout=60
        )
        
        if response.status_code != 200:
            raise Exception(f"API error: {response.text}")
        
        return response.json()["content"][0]["text"]
    
    def _deepseek_chat(self, messages: List[Dict], system_prompt: str = None) -> str:
        import requests
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        if system_prompt:
            full_messages = [{"role": "system", "content": system_prompt}] + messages
        else:
            full_messages = messages
        
        data = {
            "model": self.model,
            "messages": full_messages
        }
        
        response = requests.post(
            "https://api.deepseek.com/v1/chat/completions",
            headers=headers,
            json=data,
            timeout=60
        )
        
        if response.status_code != 200:
            raise Exception(f"API error: {response.text}")
        
        return response.json()["choices"][0]["message"]["content"]
    
    def _openrouter_chat(self, messages: List[Dict], system_prompt: str = None) -> str:
        import requests
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        if system_prompt:
            full_messages = [{"role": "system", "content": system_prompt}] + messages
        else:
            full_messages = messages
        
        data = {
            "model": self.model,
            "messages": full_messages
        }
        
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers=headers,
            json=data,
            timeout=60
        )
        
        if response.status_code != 200:
            raise Exception(f"API error: {response.text}")
        
        return response.json()["choices"][0]["message"]["content"]


def create_client(provider: str = None, model: str = None) -> APIClient:
    """创建 API 客户端"""
    # 如果未指定，自动检测
    if not provider:
        for p in APIClient.PROVIDERS:
            if os.environ.get(f"{p.upper()}_API_KEY"):
                provider = p
                break
        if not provider:
            raise ValueError("No API key found. Please set OPENAI_API_KEY or ANTHROPIC_API_KEY")
    
    return APIClient(provider=provider, model=model)