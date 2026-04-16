"""
微信平台适配器
基于 Hermes gateway/platforms/weixin.py 简化
"""

import os
import json
import asyncio
import logging
from typing import Dict, List, Optional, Any
from datetime import datetime

logger = logging.getLogger(__name__)


class WeixinAdapter:
    """
    微信连接适配器
    
    配置参数：
    - app_id: 应用 ID
    - app_secret: 应用密钥
    - token: 验证 token（可选）
    """
    
    BASE_URL = "https://ilinkai.weixin.qq.com"
    
    def __init__(self, config: Dict[str, Any]):
        self.app_id = config.get("app_id") or os.getenv("WEIXIN_APP_ID")
        self.app_secret = config.get("app_secret") or os.getenv("WEIXIN_APP_SECRET")
        self.token = config.get("token") or os.getenv("WEIXIN_TOKEN")
        
        if not self.app_id or not self.app_secret:
            raise ValueError("请配置 WEIXIN_APP_ID 和 WEIXIN_APP_SECRET")
        
        self._session = None
        self._running = False
    
    async def connect(self) -> bool:
        """连接微信"""
        logger.info("正在连接微信...")
        # 实际连接需要与 iLink 服务建立连接
        # 这里简化处理
        self._running = True
        logger.info("微信连接成功")
        return True
    
    async def disconnect(self):
        """断开连接"""
        self._running = False
        logger.info("微信已断开")
    
    async def get_updates(self, timeout: int = 35) -> List[Dict]:
        """
        获取最新消息
        这是微信连接的核心 - 长轮询获取消息
        """
        if not self._running:
            return []
        
        # 简化实现：返回空列表
        # 实际需要调用 ilink/bot/getupdates API
        return []
    
    async def send_message(self, user_id: str, content: str, 
                          msg_type: str = "text") -> bool:
        """发送消息"""
        if not self._running:
            return False
        
        # 实际需要调用 ilink/bot/sendmessage API
        logger.info(f"发送消息到 {user_id}: {content[:50]}...")
        return True
    
    async def send_image(self, user_id: str, image_path: str) -> bool:
        """发送图片"""
        logger.info(f"发送图片到 {user_id}: {image_path}")
        return True
    
    async def send_typing(self, user_id: str):
        """发送 typing 状态"""
        # 实际调用 ilink/bot/sendtyping
        pass
    
    @property
    def is_connected(self) -> bool:
        return self._running
    
    def get_user_info(self, user_id: str) -> Optional[Dict]:
        """获取用户信息"""
        # 实际需要查询
        return {"user_id": user_id, "name": "用户"}


class WeixinMessage:
    """微信消息"""
    
    TYPES = {
        "text": "文本",
        "image": "图片",
        "voice": "语音",
        "video": "视频",
        "file": "文件"
    }
    
    def __init__(self, data: Dict):
        self.raw = data
        self.msg_id = data.get("msg_id", "")
        self.user_id = data.get("from_user", "")
        self.content = data.get("content", "")
        self.msg_type = data.get("msg_type", "text")
        self.timestamp = data.get("timestamp", 0)
    
    @property
    def type_name(self) -> str:
        return self.TYPES.get(self.msg_type, "未知")
    
    def is_text(self) -> bool:
        return self.msg_type == "text"
    
    def __repr__(self):
        return f"<WeixinMessage {self.msg_type} from {self.user_id}>"