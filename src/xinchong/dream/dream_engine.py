"""
做梦引擎 - 深度做梦 + 意象层 + 清醒梦
"""

import random
import json
from datetime import datetime, timedelta
from typing import List, Dict, Optional


class DreamEngine:
    """做梦引擎 - 模拟人类睡眠时的认知活动"""
    
    # 梦的元素库
    ARCHETYPES = {
        "追求": ["追逐光", "攀登高峰", "寻找出口", "奔跑"],
        "失去": ["丢失重要东西", "牙齿掉落", "身无分文", "迷路"],
        "自由": ["飞翔", "漂浮", "游泳", "突破障碍"],
        "危险": ["坠落", "被追赶", "战斗", "自然灾害"],
        "情感": ["重逢", "离别", "喜悦", "悲伤", "恐惧"],
        "创造": ["新世界", "神奇能力", "发明", "艺术"]
    }
    
    ENVIRONMENTS = [
        "古老的城堡", "未来的都市", "森林深处", "海洋底部",
        "星空之上", "沙漠绿洲", "雪山之巅", "童年母校",
        "熟悉的老家", "陌生的城市", "废弃工厂", "花园迷宫"
    ]
    
    EMOTIONS = ["平静", "焦虑", "恐惧", "喜悦", "悲伤", "困惑", "愤怒", "惊喜"]
    
    def __init__(self, memory_system=None):
        self.memory_system = memory_system
        self.dream_history = []
        self.lucid_dreams = 0  # 清醒梦次数
    
    def generate_dream(self, context: dict = None, dream_type: str = "auto") -> dict:
        """
        生成梦境
        
        Args:
            context: 上下文（最近记忆、情绪、事件）
            dream_type: normal, nightmare, lucid, prophetic
        
        Returns:
            梦境描述
        """
        if dream_type == "auto":
            dream_type = random.choice(["normal", "normal", "lucid", "prophetic"])
        
        # 构建梦境
        dream = {
            "type": dream_type,
            "created_at": datetime.now().isoformat(),
            "elements": [],
            "emotions": [],
            "narrative": "",
            "symbols": [],
            "lucidity": 0  # 清醒度 0-10
        }
        
        # 根据 dream_type 生成不同风格
        if dream_type == "nightmare":
            dream = self._generate_nightmare(dream, context)
        elif dream_type == "lucid":
            dream = self._generate_lucid_dream(dream, context)
        elif dream_type == "prophetic":
            dream = self._generate_prophetic_dream(dream, context)
        else:
            dream = self._generate_normal_dream(dream, context)
        
        self.dream_history.append(dream)
        return dream
    
    def _generate_normal_dream(self, dream: dict, context: dict = None) -> dict:
        """普通梦境"""
        # 选择主题
        theme = random.choice(list(self.ARCHETYPES.keys()))
        elements = random.sample(self.ARCHETYPES[theme], k=random.randint(1, 3))
        
        # 选择环境
        env = random.choice(self.ENVIRONMENTS)
        
        # 选择情绪
        emotions = random.sample(self.EMOTIONS, k=random.randint(1, 2))
        
        # 构建叙事
        narrative = self._build_narrative(theme, elements, env, emotions)
        
        dream["elements"] = elements
        dream["emotions"] = emotions
        dream["narrative"] = narrative
        dream["symbols"] = self._extract_symbols(narrative)
        
        return dream
    
    def _generate_nightmare(self, dream: dict, context: dict = None) -> dict:
        """噩梦"""
        elements = random.sample(self.ARCHETYPES["危险"], k=2)
        env = random.choice(["黑暗的森林", "燃烧的建筑", "崩塌的大桥", "深不见底的黑洞"])
        emotions = ["恐惧", "焦虑", "绝望"]
        
        narrative = self._build_narrative("危险", elements, env, emotions)
        
        dream["elements"] = elements
        dream["emotions"] = emotions
        dream["narrative"] = narrative
        dream["symbols"] = self._extract_symbols(narrative)
        
        return dream
    
    def _generate_lucid_dream(self, dream: dict, context: dict = None) -> dict:
        """清醒梦 - 用户知道自己在做梦"""
        elements = random.sample(self.ARCHETYPES["自由"], k=2)
        env = random.choice(["可以飞行的城市", "水下的世界", "自我创造的空间"])
        emotions = ["惊喜", "兴奋", "平静"]
        
        narrative = f"你突然意识到自己在梦中。你可以控制这个世界的规则。{', '.join(elements)}，你在这个空间中自由探索。"
        
        dream["elements"] = elements
        dream["emotions"] = emotions
        dream["narrative"] = narrative
        dream["symbols"] = self._extract_symbols(narrative)
        dream["lucidity"] = random.randint(7, 10)
        self.lucid_dreams += 1
        
        return dream
    
    def _generate_prophetic(self, dream: dict, context: dict = None) -> dict:
        """预言梦 - 模糊的未来场景"""
        future_themes = ["新的开始", "重要的决定", "人际变化", "职业发展"]
        elements = random.sample(future_themes, k=1)
        env = random.choice(["模糊的未来城市", "未知的地方", "似曾相识的场景"])
        emotions = ["困惑", "期待", "不安"]
        
        narrative = f"这个梦境显得格外真实。你看到{'、'.join(elements)}，但一切都很模糊，像是未来的某个时刻。"
        
        dream["elements"] = elements
        dream["emotions"] = emotions
        dream["narrative"] = narrative
        dream["symbols"] = self._extract_symbols(narrative)
        dream["prophetic"] = True
        
        return dream
    
    def _build_narrative(self, theme: str, elements: List[str], 
                        env: str, emotions: List[str]) -> str:
        """构建梦境叙事"""
        templates = [
            f"你在{env}，感到{emotions[0]}。突然，{elements[0]}，你...",
            f"梦中你发现了{elements[0]}，周围是{env}，你感到{emotions[-1]}...",
            f"{env}中，你正在{elements[0]}，心中充满{emotions[0]}..."
        ]
        
        narrative = random.choice(templates)
        
        # 扩展叙事
        if len(elements) > 1:
            narrative += f" 然后，{elements[1]}。"
        
        return narrative
    
    def _extract_symbols(self, narrative: str) -> List[str]:
        """提取梦境符号"""
        symbols = []
        
        symbol_map = {
            "飞": "自由/逃避",
            "水": "情感/潜意识",
            "火": "激情/变革",
            "死亡": "结束/转化",
            "追": "压力/目标",
            "掉": "失去/焦虑",
            "门": "机会/转变",
            "路": "人生选择"
        }
        
        for char, meaning in symbol_map.items():
            if char in narrative:
                symbols.append(f"{char}: {meaning}")
        
        return symbols
    
    # ===== 梦境分析 =====
    def analyze_patterns(self) -> dict:
        """分析梦境模式"""
        if not self.dream_history:
            return {"message": "No dreams recorded yet"}
        
        # 统计情绪分布
        all_emotions = []
        for dream in self.dream_history:
            all_emotions.extend(dream.get("emotions", []))
        
        emotion_dist = {}
        for e in all_emotions:
            emotion_dist[e] = emotion_dist.get(e, 0) + 1
        
        # 统计类型
        type_dist = {}
        for dream in self.dream_history:
            t = dream.get("type", "unknown")
            type_dist[t] = type_dist.get(t, 0) + 1
        
        return {
            "total_dreams": len(self.dream_history),
            "lucid_dreams": self.lucid_dreams,
            "emotion_distribution": emotion_dist,
            "type_distribution": type_dist,
            "recent_themes": [d.get("elements", [])[0] if d.get("elements") else "unknown" 
                            for d in self.dream_history[-5:]]
        }
    
    def interpret_dream(self, dream: dict) -> dict:
        """解读梦境"""
        interpretations = []
        
        # 情绪解读
        emotions = dream.get("emotions", [])
        if "恐惧" in emotions or "焦虑" in emotions:
            interpretations.append("可能反映现实中的压力或未解决的冲突")
        if "喜悦" in emotions:
            interpretations.append("可能表示对现状的满足或对未来的期待")
        
        # 类型解读
        if dream.get("type") == "nightmare":
            interpretations.append("噩梦通常是潜意识在处理负面情绪")
        elif dream.get("type") == "lucid":
            interpretations.append("清醒梦表示你有较强的自我意识")
        
        # 元素解读
        for elem in dream.get("elements", []):
            if "飞" in elem or "漂浮" in elem:
                interpretations.append("飞翔象征对自由的渴望或超越困难的愿望")
            elif "追" in elem:
                interpretations.append("被追逐可能表示你在逃避某种责任或情绪")
        
        return {
            "dream_type": dream.get("type"),
            "emotions": emotions,
            "interpretations": interpretations,
            "symbols": dream.get("symbols", [])
        }
    
    # ===== 记忆整合 =====
    def integrate_memory(self, memory_content: str) -> dict:
        """将记忆整合到梦中"""
        # 模拟将近期记忆编织进梦境
        dream = self.generate_dream(context={"memory": memory_content})
        
        # 添加记忆元素
        dream["narrative"] += f"\n\n梦中还出现了: {memory_content[:50]}..."
        dream["integrated_memory"] = True
        
        return dream
    
    # ===== 状态查询 =====
    def get_dream_statistics(self) -> dict:
        """获取梦境统计"""
        return {
            "total": len(self.dream_history),
            "lucid_count": self.lucid_dreams,
            "by_type": {d.get("type"): 1 for d in self.dream_history}
        }


# 全局实例
dream_engine = DreamEngine()