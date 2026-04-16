"""
心虫 Agent - 独立运行的 AI 伙伴
"""

import os
import sys
from pathlib import Path

# 添加 src 到路径
sys.path.insert(0, str(Path(__file__).parent.parent))

from xinchong.agent.api_client import create_client
from xinchong.agent.conversation import ConversationManager
from xinchong.core.truth import TruthModule
from xinchong.core.goodness import GoodnessModule
from xinchong.core.beauty import BeautyModule
from xinchong.psychology.phq9 import PHQ9Module
from xinchong.psychology.gad7 import GAD7Module


class XinChongAgent:
    """
    心虫 Agent - 独立运行的 AI 伙伴
    
    特性：
    - 真善美价值观
    - 心理健康检测
    - 记忆永存
    - 持续对话
    """
    
    def __init__(self, provider: str = None, model: str = None):
        # 初始化各模块
        self.client = create_client(provider, model)
        self.conversation = ConversationManager()
        self.truth = TruthModule()
        self.goodness = GoodnessModule()
        self.beauty = BeautyModule()
        self.phq9 = PHQ9Module()
        self.gad7 = GAD7Module()
        
        # 系统提示词
        self.system_prompt = self._build_system_prompt()
        
        # 开始新会话
        self.conversation.start_session()
    
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
    
    def chat(self, user_input: str) -> str:
        """处理用户输入，返回回复"""
        
        # 1. 心理健康检测
        self._check_mental_health(user_input)
        
        # 2. 真善美检查
        tgb_result = self._tgb_check(user_input)
        
        # 3. 构建消息
        messages = self.conversation.get_messages(limit=20)
        
        # 4. 调用 API
        try:
            response = self.client.chat(messages, self.system_prompt)
        except Exception as e:
            return f"出错了: {str(e)}"
        
        # 5. 保存对话
        self.conversation.add_message("user", user_input)
        self.conversation.add_message("assistant", response)
        self.conversation.save_session()
        
        return response
    
    def _check_mental_health(self, user_input: str):
        """心理健康检测"""
        # 危机检测
        crisis = self.phq9.crisis_check(user_input)
        if crisis["has_crisis"]:
            print(f"\n⚠️ 心理危机信号: {crisis['signals']}")
            print(f"建议: {crisis['action']}\n")
        
        # 抑郁评估
        depression = self.phq9.assess(user_input)
        if depression["risk"] in ["高风险", "中高风险"]:
            print(f"\n💡 抑郁倾向: {depression['level']} - {depression['suggestion']}\n")
        
        # 焦虑评估
        anxiety = self.gad7.assess(user_input)
        if anxiety["risk"] in ["高风险", "中等风险"]:
            print(f"\n💡 焦虑倾向: {anxiety['level']} - {anxiety['suggestion']}\n")
    
    def _tgb_check(self, text: str) -> dict:
        """真善美检查"""
        truth = self.truth.check(text)
        goodness = self.goodness.check(text)
        beauty = self.beauty.check(text)
        
        tgb = 0.35 * truth["score"] + 0.35 * goodness["score"] + 0.30 * beauty["score"]
        
        return {
            "score": tgb,
            "passed": tgb >= 0.7,
            "truth": truth,
            "goodness": goodness,
            "beauty": beauty
        }
    
    def status(self) -> dict:
        """查看状态"""
        sessions = self.conversation.list_sessions(limit=5)
        return {
            "sessions": sessions,
            "current_session": self.conversation.current_session_id,
            "message_count": len(self.conversation.messages)
        }
    
    def exit(self):
        """退出并保存"""
        self.conversation.save_session()
        print("会话已保存。再见！")


def run_cli():
    """运行 CLI"""
    print("=" * 50)
    print("🐛 心虫 Agent - 独立运行的 AI 伙伴")
    print("=" * 50)
    print("输入内容开始对话，输入 'status' 查看状态，输入 'exit' 退出")
    print()
    
    # 初始化
    try:
        agent = XinChongAgent()
    except ValueError as e:
        print(f"错误: {e}")
        print("\n请设置环境变量:")
        print("  export OPENAI_API_KEY=your_key")
        print("  或")
        print("  export ANTHROPIC_API_KEY=your_key")
        sys.exit(1)
    
    print(f"会话已开启: {agent.conversation.current_session_id}")
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
            
            response = agent.chat(user_input)
            print(f"\n心虫: {response}")
            
        except KeyboardInterrupt:
            print("\n\n退出中...")
            agent.exit()
            break
        except Exception as e:
            print(f"错误: {e}")


if __name__ == "__main__":
    run_cli()