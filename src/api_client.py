# API Client — Multi-provider LLM abstraction
# Supports: OpenAI, Anthropic, OpenRouter, Ollama, Gemini

import os
import json
import time
import requests
from typing import Dict, List, Optional, Any, Generator, Tuple
from dataclasses import dataclass, field
from abc import ABC, abstractmethod

DEFAULT_TIMEOUT = 120


# ============================================================
# Provider ABC
# ============================================================

class LLMProvider(ABC):
    """Abstract base class for LLM providers"""

    @abstractmethod
    def chat(self, messages: List[Dict], **kwargs) -> Tuple[str, str]:
        """Send chat request, return (content, model_used)"""
        pass

    @abstractmethod
    def chat_stream(self, messages: List[Dict], **kwargs) -> Generator[str, None, None]:
        """Stream chat response"""
        pass

    @abstractmethod
    def get_default_model(self) -> str:
        """Get the default model name"""
        pass


# ============================================================
# OpenAI Provider
# ============================================================

class OpenAIProvider(LLMProvider):
    def __init__(self, api_key: str, base_url: str, default_model: str, timeout: int = DEFAULT_TIMEOUT):
        self.api_key = api_key or os.environ.get("OPENAI_API_KEY", "")
        self.base_url = base_url or "https://api.openai.com/v1"
        self.default_model = default_model or "gpt-4o-mini"
        self.timeout = timeout

    def chat(self, messages: List[Dict], model: str = None, temperature: float = 0.7,
             max_tokens: int = 4096, **kwargs) -> Tuple[str, str]:
        url = f"{self.base_url.rstrip('/')}/chat/completions"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        payload = {
            "model": model or self.default_model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
            **kwargs,
        }
        resp = requests.post(url, headers=headers, json=payload, timeout=self.timeout)
        resp.raise_for_status()
        data = resp.json()
        return data["choices"][0]["message"]["content"], data["model"]

    def chat_stream(self, messages: List[Dict], model: str = None, temperature: float = 0.7,
                    max_tokens: int = 4096, **kwargs) -> Generator[str, None, None]:
        url = f"{self.base_url.rstrip('/')}/chat/completions"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        payload = {
            "model": model or self.default_model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
            "stream": True,
            **kwargs,
        }
        with requests.post(url, headers=headers, json=payload, stream=True, timeout=self.timeout) as r:
            r.raise_for_status()
            for line in r.iter_lines():
                if line:
                    line = line.decode("utf-8")
                    if line.startswith("data: "):
                        data = line[6:]
                        if data == "[DONE]":
                            break
                        try:
                            obj = json.loads(data)
                            delta = obj["choices"][0].get("delta", {})
                            content = delta.get("content", "")
                            if content:
                                yield content
                        except json.JSONDecodeError:
                            pass

    def get_default_model(self) -> str:
        return self.default_model


# ============================================================
# Anthropic Provider
# ============================================================

class AnthropicProvider(LLMProvider):
    def __init__(self, api_key: str, base_url: str, default_model: str, timeout: int = DEFAULT_TIMEOUT):
        self.api_key = api_key or os.environ.get("ANTHROPIC_API_KEY", "")
        self.base_url = base_url or "https://api.anthropic.com/v1"
        self.default_model = default_model or "claude-sonnet-4-7a570a"
        self.timeout = timeout

    def _to_anthropic_format(self, messages: List[Dict]) -> Tuple[str, List[Dict]]:
        """Convert OpenAI format to Anthropic format"""
        system = ""
        anthropic_msgs = []
        for msg in messages:
            role = msg["role"]
            content = msg["content"]
            if role == "system":
                system = content
            elif role == "user":
                anthropic_msgs.append({"role": "user", "content": content})
            elif role == "assistant":
                anthropic_msgs.append({"role": "assistant", "content": content})
        return system, anthropic_msgs

    def chat(self, messages: List[Dict], model: str = None, temperature: float = 0.7,
             max_tokens: int = 4096, **kwargs) -> Tuple[str, str]:
        url = f"{self.base_url.rstrip('/')}/messages"
        system_prompt, anthropic_msgs = self._to_anthropic_format(messages)
        headers = {
            "x-api-key": self.api_key,
            "anthropic-version": "2023-06-01",
            "Content-Type": "application/json",
        }
        payload = {
            "model": model or self.default_model,
            "messages": anthropic_msgs,
            "temperature": temperature,
            "max_tokens": max_tokens,
        }
        if system_prompt:
            payload["system"] = system_prompt
        resp = requests.post(url, headers=headers, json=payload, timeout=self.timeout)
        resp.raise_for_status()
        data = resp.json()
        return data["content"][0]["text"], data["model"]

    def chat_stream(self, messages: List[Dict], model: str = None, temperature: float = 0.7,
                    max_tokens: int = 4096, **kwargs) -> Generator[str, None, None]:
        # Anthropic streaming via SSE
        url = f"{self.base_url.rstrip('/')}/messages"
        system_prompt, anthropic_msgs = self._to_anthropic_format(messages)
        headers = {
            "x-api-key": self.api_key,
            "anthropic-version": "2023-06-01",
            "Content-Type": "application/json",
        }
        payload = {
            "model": model or self.default_model,
            "messages": anthropic_msgs,
            "temperature": temperature,
            "max_tokens": max_tokens,
            "stream": True,
        }
        if system_prompt:
            payload["system"] = system_prompt
        with requests.post(url, headers=headers, json=payload, stream=True, timeout=self.timeout) as r:
            r.raise_for_status()
            for line in r.iter_lines():
                if line:
                    line = line.decode("utf-8")
                    if line.startswith("data: "):
                        data = line[6:]
                        if data == "[DONE]":
                            break
                        try:
                            obj = json.loads(data)
                            if obj.get("type") == "content_block_delta":
                                delta = obj.get("delta", {})
                                if delta.get("type") == "text_delta":
                                    yield delta.get("text", "")
                        except json.JSONDecodeError:
                            pass

    def get_default_model(self) -> str:
        return self.default_model


# ============================================================
# OpenRouter Provider
# ============================================================

class OpenRouterProvider(LLMProvider):
    def __init__(self, api_key: str, base_url: str, default_model: str, timeout: int = DEFAULT_TIMEOUT):
        self.api_key = api_key or os.environ.get("OPENROUTER_API_KEY", "")
        self.base_url = base_url or "https://openrouter.ai/api/v1"
        self.default_model = default_model or "anthropic/claude-sonnet-4"
        self.timeout = timeout

    def chat(self, messages: List[Dict], model: str = None, temperature: float = 0.7,
             max_tokens: int = 4096, **kwargs) -> Tuple[str, str]:
        url = f"{self.base_url.rstrip('/')}/chat/completions"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://xinchong.app",
            "X-Title": "心虫 (Xinchong)",
        }
        payload = {
            "model": model or self.default_model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
            **kwargs,
        }
        resp = requests.post(url, headers=headers, json=payload, timeout=self.timeout)
        resp.raise_for_status()
        data = resp.json()
        return data["choices"][0]["message"]["content"], data["model"]

    def chat_stream(self, messages: List[Dict], model: str = None, temperature: float = 0.7,
                    max_tokens: int = 4096, **kwargs) -> Generator[str, None, None]:
        url = f"{self.base_url.rstrip('/')}/chat/completions"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://xinchong.app",
            "X-Title": "心虫 (Xinchong)",
        }
        payload = {
            "model": model or self.default_model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
            "stream": True,
            **kwargs,
        }
        with requests.post(url, headers=headers, json=payload, stream=True, timeout=self.timeout) as r:
            r.raise_for_status()
            for line in r.iter_lines():
                if line:
                    line = line.decode("utf-8")
                    if line.startswith("data: "):
                        data = line[6:]
                        if data == "[DONE]":
                            break
                        try:
                            obj = json.loads(data)
                            delta = obj["choices"][0].get("delta", {})
                            content = delta.get("content", "")
                            if content:
                                yield content
                        except json.JSONDecodeError:
                            pass

    def get_default_model(self) -> str:
        return self.default_model


# ============================================================
# Ollama Provider (local)
# ============================================================

class OllamaProvider(LLMProvider):
    def __init__(self, api_key: str, base_url: str, default_model: str, timeout: int = DEFAULT_TIMEOUT):
        self.api_key = api_key
        self.base_url = base_url or "http://localhost:11434/v1"
        self.default_model = default_model or "llama3"
        self.timeout = timeout

    def chat(self, messages: List[Dict], model: str = None, temperature: float = 0.7,
             max_tokens: int = 4096, **kwargs) -> Tuple[str, str]:
        url = f"{self.base_url.rstrip('/')}/chat/completions"
        headers = {"Content-Type": "application/json"}
        payload = {
            "model": model or self.default_model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
        }
        resp = requests.post(url, headers=headers, json=payload, timeout=self.timeout)
        resp.raise_for_status()
        data = resp.json()
        return data["choices"][0]["message"]["content"], data["model"]

    def chat_stream(self, messages: List[Dict], model: str = None, temperature: float = 0.7,
                    max_tokens: int = 4096, **kwargs) -> Generator[str, None, None]:
        url = f"{self.base_url.rstrip('/')}/chat/completions"
        headers = {"Content-Type": "application/json"}
        payload = {
            "model": model or self.default_model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
            "stream": True,
        }
        with requests.post(url, headers=headers, json=payload, stream=True, timeout=self.timeout) as r:
            r.raise_for_status()
            for line in r.iter_lines():
                if line:
                    line = line.decode("utf-8")
                    if line.startswith("data: "):
                        data = line[6:]
                        if data == "[DONE]":
                            break
                        try:
                            obj = json.loads(data)
                            delta = obj["choices"][0].get("delta", {})
                            content = delta.get("content", "")
                            if content:
                                yield content
                        except json.JSONDecodeError:
                            pass

    def get_default_model(self) -> str:
        return self.default_model


# ============================================================
# API Client Factory
# ============================================================

class APIClient:
    """
    Unified API client that routes to the appropriate provider.
    Supports: openai, anthropic, openrouter, ollama, gemini
    """

    PROVIDERS = {
        "openai": OpenAIProvider,
        "anthropic": AnthropicProvider,
        "openrouter": OpenRouterProvider,
        "ollama": OllamaProvider,
    }

    def __init__(self, config: Dict):
        self.config = config
        self.providers: Dict[str, LLMProvider] = {}
        self.default_provider = config.get("default_provider", "openai")
        self._init_providers()

    def _init_providers(self):
        """Initialize all configured providers"""
        providers_cfg = self.config.get("providers", {})
        for name, cfg in providers_cfg.items():
            if name in self.PROVIDERS:
                # Expand env vars
                api_key = cfg.get("api_key", "")
                if api_key.startswith("${") and api_key.endswith("}"):
                    env_var = api_key[2:-1]
                    api_key = os.environ.get(env_var, "")
                self.providers[name] = self.PROVIDERS[name](
                    api_key=api_key,
                    base_url=cfg.get("base_url", ""),
                    default_model=cfg.get("default_model", ""),
                    timeout=cfg.get("timeout", DEFAULT_TIMEOUT),
                )

    def chat(self, messages: List[Dict], provider: str = None, **kwargs) -> Tuple[str, str]:
        """Send a chat request"""
        provider = provider or self.default_provider
        if provider not in self.providers:
            raise ValueError(f"Unknown provider: {provider}. Available: {list(self.providers.keys())}")
        return self.providers[provider].chat(messages, **kwargs)

    def chat_stream(self, messages: List[Dict], provider: str = None, **kwargs) -> Generator[str, None, None]:
        """Stream a chat response"""
        provider = provider or self.default_provider
        if provider not in self.providers:
            raise ValueError(f"Unknown provider: {provider}")
        yield from self.providers[provider].chat_stream(messages, **kwargs)

    def list_providers(self) -> List[str]:
        """List available (configured) providers"""
        return list(self.providers.keys())

    def get_default_provider(self) -> str:
        return self.default_provider

    def is_provider_available(self, provider: str) -> bool:
        return provider in self.providers
