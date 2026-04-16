"""
API 客户端 - 支持多 provider (扩展版)
"""

import os
import json
from typing import Optional, List, Dict


class APIClient:
    """API 客户端，支持多 provider"""
    
    # 所有支持的 provider
    PROVIDERS = [
        # 国际
        "openai", "anthropic", "deepseek", "openrouter", "google", "xai", "cohere",
        # 国内
        "minimax", "douyin", "wenxin", "tongyi", "hunyuan", "spark", "zhipu",
        # 其他
        "opencode", "opencode-go"
    ]
    
    # 默认模型
    DEFAULT_MODELS = {
        "openai": "gpt-4o",
        "anthropic": "claude-sonnet-4-20250514",
        "deepseek": "deepseek-chat",
        "openrouter": "anthropic/claude-sonnet-4",
        "google": "gemini-2.0-flash",
        "xai": "grok-2",
        "cohere": "command-r-plus",
        # 国内
        "minimax": "abab6.5s-chat",
        "douyin": "douyin-pro-32k",
        "wenxin": "ernie-4.0-8k",
        "tongyi": "qwen-plus",
        "hunyuan": "hunyuan-pro",
        "spark": "spark-pro",
        "zhipu": "glm-4",
        # OpenCode
        "opencode": "deepseek-chat",
        "opencode-go": "deepseek-chat"
    }
    
    # API 端点
    ENDPOINTS = {
        "openai": "https://api.openai.com/v1/chat/completions",
        "anthropic": "https://api.anthropic.com/v1/messages",
        "deepseek": "https://api.deepseek.com/v1/chat/completions",
        "openrouter": "https://openrouter.ai/api/v1/chat/completions",
        "google": "https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent",
        "xai": "https://api.x.ai/v1/chat/completions",
        "cohere": "https://api.cohere.ai/v1/chat",
        # 国内
        "minimax": "https://api.minimax.chat/v1/text/chatcompletion_pro",
        "douyin": "https://ark.cn-beijing.volces.com/api/v3/chat/completions",
        "wenxin": "https://qianfan.baidubce.com/v2/chat/completions",
        "tongyi": "https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation",
        "hunyuan": "https://hunyuan.tencentcloudapi.com/v3/text/chatcompletion",
        "spark": "wss://spark-api.xf-yun.com/v3.5/chat",
        "zhipu": "https://open.bigmodel.cn/api/paas/v4/chat/completions",
        # OpenCode
        "opencode": "https://opencode.cn/v1/chat/completions",
        "opencode-go": "https://opencode.cn/v1/chat/completions"
    }
    
    def __init__(self, provider: str = "openai", model: str = None):
        self.provider = provider.lower()
        self.model = model or self.DEFAULT_MODELS.get(self.provider, "gpt-4o")
        self.api_key = self._get_api_key()
        self.api_base = os.environ.get(f"{self.provider.upper()}_API_BASE", "")
    
    def _get_api_key(self) -> str:
        """获取 API key"""
        env_vars = {
            "openai": "OPENAI_API_KEY",
            "anthropic": "ANTHROPIC_API_KEY",
            "deepseek": "DEEPSEEK_API_KEY",
            "openrouter": "OPENROUTER_API_KEY",
            "google": "GOOGLE_API_KEY",
            "xai": "XAI_API_KEY",
            "cohere": "COHERE_API_KEY",
            # 国内
            "minimax": "MINIMAX_API_KEY",
            "douyin": "DOUYIN_API_KEY",
            "wenxin": "WENXIN_API_KEY",
            "tongyi": "TONGYI_API_KEY",
            "hunyuan": "HUNYUAN_API_KEY",
            "spark": "SPARK_API_KEY",
            "zhipu": "ZHIPU_API_KEY",
            # OpenCode
            "opencode": "OPENCODE_ZEN_API_KEY",
            "opencode-go": "OPENCODE_ZEN_API_KEY"
        }
        
        key = os.environ.get(env_vars.get(self.provider, ""))
        if not key:
            raise ValueError(f"Please set {env_vars[self.provider]} environment variable")
        return key
    
    def chat(self, messages: List[Dict], system_prompt: str = None) -> str:
        """发送对话请求"""
        # 分发到对应 provider
        method_name = f"_{self.provider}_chat"
        if hasattr(self, method_name):
            return getattr(self, method_name)(messages, system_prompt)
        else:
            return self._openai_style_chat(messages, system_prompt)
    
    # ===== OpenAI 风格 (OpenAI, DeepSeek, OpenRouter, Google, xAI) =====
    def _openai_style_chat(self, messages: List[Dict], system_prompt: str = None) -> str:
        import requests
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        # 合并 system prompt
        full_messages = []
        if system_prompt:
            full_messages.append({"role": "system", "content": system_prompt})
        full_messages.extend(messages)
        
        data = {
            "model": self.model,
            "messages": full_messages,
            "temperature": 0.7
        }
        
        endpoint = self.ENDPOINTS.get(self.provider, "")
        response = requests.post(endpoint, headers=headers, json=data, timeout=60)
        
        if response.status_code != 200:
            raise Exception(f"API error: {response.text}")
        
        result = response.json()
        return result["choices"][0]["message"]["content"]
    
    # ===== Anthropic =====
    def _anthropic_chat(self, messages: List[Dict], system_prompt: str = None) -> str:
        import requests
        
        headers = {
            "x-api-key": self.api_key,
            "Content-Type": "application/json",
            "anthropic-version": "2023-06-01"
        }
        
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
            self.ENDPOINTS["anthropic"],
            headers=headers,
            json=data,
            timeout=60
        )
        
        if response.status_code != 200:
            raise Exception(f"API error: {response.text}")
        
        return response.json()["content"][0]["text"]
    
    # ===== MiniMax (国内) =====
    def _minimax_chat(self, messages: List[Dict], system_prompt: str = None) -> str:
        import requests
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        # MiniMax 格式
        full_messages = []
        if system_prompt:
            full_messages.append({"role": "system", "content": system_prompt})
        full_messages.extend(messages)
        
        data = {
            "model": self.model,
            "messages": full_messages,
            "temperature": 0.7
        }
        
        response = requests.post(
            self.ENDPOINTS["minimax"],
            headers=headers,
            json=data,
            timeout=60
        )
        
        if response.status_code != 200:
            raise Exception(f"API error: {response.text}")
        
        result = response.json()
        return result["choices"][0]["message"]["content"]
    
    # ===== 百度文心 =====
    def _wenxin_chat(self, messages: List[Dict], system_prompt: str = None) -> str:
        import requests
        
        # 百度需要 access token，先获取
        # 这里简化处理，实际需要先获取 token
        headers = {
            "Content-Type": "application/json"
        }
        
        # 转换消息格式
        full_messages = []
        if system_prompt:
            full_messages.append({"role": "user", "content": system_prompt})
        full_messages.extend(messages)
        
        data = {
            "model": self.model,
            "messages": full_messages
        }
        
        # 实际应该用 access token
        response = requests.post(
            self.ENDPOINTS["wenxin"],
            headers=headers,
            json=data,
            timeout=60
        )
        
        if response.status_code != 200:
            raise Exception(f"API error: {response.text}")
        
        result = response.json()
        return result["result"]
    
    # ===== 阿里通义 =====
    def _tongyi_chat(self, messages: List[Dict], system_prompt: str = None) -> str:
        import requests
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        full_messages = []
        if system_prompt:
            full_messages.append({"role": "system", "content": system_prompt})
        full_messages.extend(messages)
        
        data = {
            "model": self.model,
            "input": {"messages": full_messages}
        }
        
        response = requests.post(
            self.ENDPOINTS["tongyi"],
            headers=headers,
            json=data,
            timeout=60
        )
        
        if response.status_code != 200:
            raise Exception(f"API error: {response.text}")
        
        result = response.json()
        return result["output"]["text"]
    
    # ===== 腾讯混元 =====
    def _hunyuan_chat(self, messages: List[Dict], system_prompt: str = None) -> str:
        import requests
        
        headers = {
            "Content-Type": "application/json"
        }
        
        full_messages = []
        if system_prompt:
            full_messages.append({"role": "system", "content": system_prompt})
        full_messages.extend(messages)
        
        data = {
            "model": self.model,
            "messages": full_messages
        }
        
        response = requests.post(
            self.ENDPOINTS["hunyuan"],
            headers=headers,
            json=data,
            timeout=60
        )
        
        if response.status_code != 200:
            raise Exception(f"API error: {response.text}")
        
        result = response.json()
        return result["choices"][0]["message"]["content"]
    
    # ===== 讯飞星火 =====
    def _spark_chat(self, messages: List[Dict], system_prompt: str = None) -> str:
        import requests
        import base64
        import hmac
        import hashlib
        import time
        import json
        
        # 讯飞使用 WebSocket，这里简化为 HTTP 调用
        # 实际需要使用 websocket-client
        
        headers = {"Content-Type": "application/json"}
        
        full_messages = []
        if system_prompt:
            full_messages.append({"role": "system", "content": system_prompt})
        full_messages.extend(messages)
        
        data = {
            "header": {
                "app_id": self.api_key.split(":")[0] if ":" in self.api_key else ""
            },
            "parameter": {"chat": {"domain": "generalv3.5", "temperature": 0.5}},
            "payload": {"message": {"text": full_messages}}
        }
        
        response = requests.post(
            "https://spark-api.xf-yun.com/v3.5/chat",
            headers=headers,
            json=data,
            timeout=60
        )
        
        if response.status_code != 200:
            raise Exception(f"API error: {response.text}")
        
        result = response.json()
        return result["payload"]["choices"]["text"][0]["content"]
    
    # ===== 智谱 GLM =====
    def _zhipu_chat(self, messages: List[Dict], system_prompt: str = None) -> str:
        import requests
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        full_messages = []
        if system_prompt:
            full_messages.append({"role": "system", "content": system_prompt})
        full_messages.extend(messages)
        
        data = {
            "model": self.model,
            "messages": full_messages
        }
        
        response = requests.post(
            self.ENDPOINTS["zhipu"],
            headers=headers,
            json=data,
            timeout=60
        )
        
        if response.status_code != 200:
            raise Exception(f"API error: {response.text}")
        
        result = response.json()
        return result["choices"][0]["message"]["content"]
    
    # ===== 豆包 =====
    def _douyin_chat(self, messages: List[Dict], system_prompt: str = None) -> str:
        return self._openai_style_chat(messages, system_prompt)
    
    # ===== Google =====
    def _google_chat(self, messages: List[Dict], system_prompt: str = None) -> str:
        import requests
        
        # Google 使用不同的端点格式
        headers = {"Content-Type": "application/json"}
        
        # 合并消息
        content = ""
        if system_prompt:
            content += f"System: {system_prompt}\n"
        for m in messages:
            content += f"{m['role']}: {m['content']}\n"
        
        data = {
            "contents": [{"parts": [{"text": content}]}],
            "generationConfig": {"temperature": 0.7}
        }
        
        endpoint = self.ENDPOINTS["google"].format(model=self.model)
        response = requests.post(endpoint, headers=headers, json=data, timeout=60)
        
        if response.status_code != 200:
            raise Exception(f"API error: {response.text}")
        
        result = response.json()
        return result["candidates"][0]["content"]["parts"][0]["text"]
    
    # ===== xAI =====
    def _xai_chat(self, messages: List[Dict], system_prompt: str = None) -> str:
        return self._openai_style_chat(messages, system_prompt)
    
    # ===== Cohere =====
    def _cohere_chat(self, messages: List[Dict], system_prompt: str = None) -> str:
        import requests
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        # 合并消息
        chat_history = []
        if system_prompt:
            chat_history.append({"role": "system", "content": system_prompt})
        chat_history.extend(messages[:-1])
        
        data = {
            "model": self.model,
            "chat_history": chat_history,
            "message": messages[-1]["content"] if messages else ""
        }
        
        response = requests.post(
            self.ENDPOINTS["cohere"],
            headers=headers,
            json=data,
            timeout=60
        )
        
        if response.status_code != 200:
            raise Exception(f"API error: {response.text}")
        
        result = response.json()
        return result["text"]


def create_client(provider: str = None, model: str = None) -> APIClient:
    """创建 API 客户端"""
    # 如果未指定，自动检测可用的 provider
    if not provider:
        for p in APIClient.PROVIDERS:
            if os.environ.get(f"{p.upper()}_API_KEY"):
                provider = p
                break
        if not provider:
            raise ValueError("No API key found. Please set one of: OPENAI_API_KEY, ANTHROPIC_API_KEY, etc.")
    
    return APIClient(provider=provider, model=model)


def list_available_providers() -> List[str]:
    """列出可用的 providers"""
    available = []
    for p in APIClient.PROVIDERS:
        if os.environ.get(f"{p.upper()}_API_KEY"):
            available.append(p)
    return available