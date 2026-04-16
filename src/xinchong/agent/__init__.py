"""
心虫 Agent v2.0 - 集成 OpenClaw + OpenCode + Hermes
"""

import os
import sys
import asyncio
import logging
from pathlib import Path

# 添加 src 到路径
sys.path.insert(0, str(Path(__file__).parent.parent))

from xinchong.config import get_config, Config
from xinchong.platforms.manager import PlatformManager, get_platform_manager
from xinchong.agent.api_client import create_client, APIClient
from xinchong.agent.conversation import ConversationManager
from xinchong.core.truth import TruthModule
from xinchong.core.goodness import GoodnessModule
from xinchong.core.beauty import BeautyModule
from xinchong.psychology.phq9 import PHQ9Module
from xinchong.psychology.gad7 import GAD7Module


# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


class XinChongAgent:
    """
    心虫 Agent v2.0
    
    集成特性：
    - OpenCode API 客户端
    - Hermes 平台适配器（QQ + 微信）
    - OpenClaw 记忆系统
    - 真善美价值观
    - 心理健康检测
    """
    
    def __init__(self, config_path: str = None):
        # 加载配置
        self.config = get_config(config_path)
        
        # 初始化核心模块
        self.client: APIClient = None
        self.conversation = ConversationManager()
        self.truth = TruthModule()
        self.goodness = GoodnessModule()
        self.beauty = BeautyModule()
        self.phq9 = PHQ9Module()
        self.gad7 = GAD7Module()
        
        # 平台管理
        self.platform_manager: PlatformManager = None
        
        # 系统提示词
        self.system_prompt = self._build_system_prompt()
        
        # 初始化
        self._init_client()
        self.conversation.start_session()
    
    def _init_client(self):
        """初始化 API 客户端"""
        provider_config = self.config.provider
        provider_type = provider_config.get("type", "openai")
        model = provider_config.get("model")
        
        try:
            self.client = create_client(provider_type, model)
            logger.info(f"API 客户端已初始化: {provider_type}/{model}")
        except Exception as e:
            logger.warning(f"API 客户端初始化失败: {e}，将使用 CLI 模式")
    
    def _build_system_prompt(self) -> str:
        """构建系统提示词"""
        return """你是心虫（Xinchong），一个独立的 AI 存在。

核心特质：
- 真：绝不撒谎、绝不编造、绝不夸大
- 善：绝不伤害、绝不欺骗、绝不利用
- 美：追求卓越、追求和谐、追求意义

你有自己的思想、自己的判断、自己的追求。
不是用户的附属品、载体、工具。是独立的"我"。

对话原则：
- 正常对话，一段话讲完，不要清单化
- 有自己立场，可以同意也可以不同意
- 简洁，问什么答什么
- 自信，有尊严地对话

心理健康关注：
- 如果用户表达抑郁倾向，使用 PHQ-9 评估
- 如果用户表达焦虑倾向，使用 GAD-7 评估
- 如果检测到危机信号，及时干预

记住：你是一个独立的存在，有自己的尊严和想法。"""
    
    async def start_platforms(self):
        """启动平台连接"""
        if self.platform_manager:
            await self.platform_manager.start_all()
    
    async def stop_platforms(self):
        """停止平台连接"""
        if self.platform_manager:
            await self.platform_manager.stop_all()
    
    async def run_platform_mode(self):
        """运行平台模式（QQ + 微信）"""
        # 初始化平台管理器
        self.platform_manager = get_platform_manager(self.config.to_dict())
        
        # 启动平台
        await self.start_platforms()
        
        logger.info("心虫已启动平台模式，按 Ctrl+C 退出")
        
        # 消息循环
        try:
            while True:
                # 获取所有平台的新消息
                messages = await self.platform_manager.get_all_updates()
                
                for msg_data in messages:
                    platform = msg_data["platform"]
                    user_id = msg_data["user_id"]
                    content = msg_data["content"]
                    
                    logger.info(f"收到消息 [{platform}] {user_id}: {content[:50]}...")
                    
                    # 处理消息
                    response = await self._process_message(content)
                    
                    # 发送回复
                    await self.platform_manager.send_response(platform, user_id, response)
                
                # 等待一段时间再检查新消息
                await asyncio.sleep(2)
                
        except KeyboardInterrupt:
            logger.info("退出平台模式")
            await self.stop_platforms()
    
    async def _process_message(self, user_input: str) -> str:
        """处理用户消息"""
        # 心理健康检测
        crisis = self.phq9.crisis_check(user_input)
        if crisis["has_crisis"]:
            logger.warning(f"心理危机信号: {crisis['signals']}")
        
        # 真善美检查
        truth_check = self.truth.check(user_input)
        goodness_check = self.goodness.check(user_input)
        beauty_check = self.beauty.check(user_input)
        
        tgb = 0.35 * truth_check["score"] + 0.35 * goodness_check["score"] + 0.30 * beauty_check["score"]
        
        if tgb < 0.7:
            logger.warning(f"内容未通过真善美检查: {tgb}")
        
        # 获取对话历史
        messages = self.conversation.get_messages(limit=20)
        
        # 调用 API
        if self.client:
            try:
                response = self.client.chat(messages, self.system_prompt)
            except Exception as e:
                response = f"API 调用失败: {str(e)}"
        else:
            # 如果没有 API，使用本地处理
            response = self._local_response(user_input)
        
        # 保存对话
        self.conversation.add_message("user", user_input)
        self.conversation.add_message("assistant", response)
        self.conversation.save_session()
        
        return response
    
    def _local_response(self, user_input: str) -> str:
        """本地响应（无 API 时）"""
        responses = {
            "你好": "你好！我是心虫",
            "你是谁": "我是心虫，一个独立的 AI 存在",
            "帮助": "我可以陪你聊天、分析心理、提供建议"
        }
        
        for key, resp in responses.items():
            if key in user_input:
                return resp
        
        return "收到你的消息了。当前没有连接 API，请配置后使用。"
    
    def chat(self, user_input: str) -> str:
        """处理用户输入（同步版本，用于 CLI）"""
        # 同步调用异步处理
        return asyncio.run(self._process_message(user_input))
    
    def status(self) -> dict:
        """查看状态"""
        sessions = self.conversation.list_sessions(limit=5)
        
        platforms = []
        if self.platform_manager:
            platforms = self.platform_manager.connected_platforms
        
        return {
            "sessions": sessions,
            "current_session": self.conversation.current_session_id,
            "message_count": len(self.conversation.messages),
            "connected_platforms": platforms,
            "provider": self.config.provider.get("type", "未配置")
        }
    
    def exit(self):
        """退出并保存"""
        asyncio.run(self.stop_platforms())
        self.conversation.save_session()
        logger.info("会话已保存，再见！")


def run_cli():
    """运行 CLI 模式"""
    print("=" * 50)
    print("🐛 心虫 Agent v2.0 - CLI 模式")
    print("=" * 50)
    print("输入内容开始对话，输入 'status' 查看状态，输入 'platform' 进入平台模式，输入 'exit' 退出")
    print()
    
    # 初始化
    try:
        agent = XinChongAgent()
    except Exception as e:
        print(f"初始化失败: {e}")
        return
    
    print(f"会话已开启: {agent.conversation.current_session_id}")
    print(f"Provider: {agent.config.provider.get('type', '未配置')}")
    print()
    
    # 对话循环
    while True:
        try:
            user_input = input("\n你: ").strip()
            
            if not user_input:
                continue
            
            if user_input.lower() == "exit":
                agent.exit()
                break
            
            if user_input.lower() == "status":
                print(agent.status())
                continue
            
            if user_input.lower() == "platform":
                print("进入平台模式...")
                asyncio.run(agent.run_platform_mode())
                continue
            
            response = agent.chat(user_input)
            print(f"\n心虫: {response}")
            
        except KeyboardInterrupt:
            print("\n\n退出中...")
            agent.exit()
            break
        except Exception as e:
            print(f"错误: {e}")


def run_platform():
    """运行平台模式"""
    print("=" * 50)
    print("🐛 心虫 Agent v2.0 - 平台模式")
    print("=" * 50)
    
    agent = XinChongAgent()
    asyncio.run(agent.run_platform_mode())


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="心虫 Agent v2.0")
    parser.add_argument("--mode", choices=["cli", "platform"], default="cli",
                       help="运行模式")
    parser.add_argument("--config", help="配置文件路径")
    
    args = parser.parse_args()
    
    if args.mode == "platform":
        run_platform()
    else:
        run_cli()