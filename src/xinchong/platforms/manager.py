"""
平台管理器 - 统一管理 QQ 和微信连接
"""

import asyncio
import logging
from typing import Dict, List, Optional, Any

from xinchong.platforms.weixin import WeixinAdapter, WeixinMessage
from xinchong.platforms.qq import QQAdapter, QQMessage

logger = logging.getLogger(__name__)


class PlatformManager:
    """
    平台连接管理器
    
    支持：
    - 微信 (weixin)
    - QQ (qq)
    """
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.platforms: Dict[str, Any] = {}
        self._running = False
    
    async def start_all(self):
        """启动所有启用的平台"""
        logger.info("启动平台连接...")
        
        platform_config = self.config.get("platforms", {})
        
        # 启动微信
        if platform_config.get("weixin", {}).get("enabled"):
            try:
                weixin = WeixinAdapter(platform_config["weixin"])
                await weixin.connect()
                self.platforms["weixin"] = weixin
                logger.info("✅ 微信已连接")
            except Exception as e:
                logger.error(f"❌ 微信连接失败: {e}")
        
        # 启动 QQ
        if platform_config.get("qq", {}).get("enabled"):
            try:
                qq = QQAdapter(platform_config["qq"])
                await qq.connect()
                self.platforms["qq"] = qq
                logger.info("✅ QQ 已连接")
            except Exception as e:
                logger.error(f"❌ QQ 连接失败: {e}")
        
        self._running = True
        logger.info(f"平台启动完成，已连接: {list(self.platforms.keys())}")
    
    async def stop_all(self):
        """停止所有平台"""
        logger.info("停止平台连接...")
        
        for name, platform in self.platforms.items():
            try:
                await platform.disconnect()
                logger.info(f"✅ {name} 已断开")
            except Exception as e:
                logger.error(f"❌ {name} 断开失败: {e}")
        
        self.platforms = {}
        self._running = False
    
    async def get_all_updates(self) -> List[Dict]:
        """获取所有平台的新消息"""
        all_messages = []
        
        # 微信消息
        weixin = self.platforms.get("weixin")
        if weixin and weixin.is_connected:
            try:
                updates = await weixin.get_updates()
                for msg in updates:
                    all_messages.append({
                        "platform": "weixin",
                        "message": WeixinMessage(msg),
                        "user_id": msg.get("from_user", ""),
                        "content": msg.get("content", "")
                    })
            except Exception as e:
                logger.error(f"获取微信消息失败: {e}")
        
        # QQ 消息
        qq = self.platforms.get("qq")
        if qq and qq.is_connected:
            try:
                updates = await qq.get_updates()
                for msg in updates:
                    all_messages.append({
                        "platform": "qq",
                        "message": QQMessage(msg),
                        "user_id": msg.get("author", {}).get("id", ""),
                        "content": msg.get("content", "")
                    })
            except Exception as e:
                logger.error(f"获取 QQ 消息失败: {e}")
        
        return all_messages
    
    async def send_response(self, platform: str, user_id: str, content: str):
        """发送回复"""
        if platform == "weixin":
            platform_obj = self.platforms.get("weixin")
            if platform_obj:
                await platform_obj.send_message(user_id, content)
        
        elif platform == "qq":
            platform_obj = self.platforms.get("qq")
            if platform_obj:
                # 判断是频道还是私信
                # 这里简化处理，发送到频道
                await platform_obj.send_message(user_id, content)
    
    @property
    def connected_platforms(self) -> List[str]:
        return [name for name, p in self.platforms.items() if p.is_connected]
    
    def get_platform(self, name: str) -> Optional[Any]:
        """获取指定平台"""
        return self.platforms.get(name)
    
    def is_running(self) -> bool:
        return self._running


# 全局实例
_platform_manager = None


def get_platform_manager(config: Dict = None) -> PlatformManager:
    """获取平台管理器实例"""
    global _platform_manager
    if _platform_manager is None:
        _platform_manager = PlatformManager(config or {})
    return _platform_manager