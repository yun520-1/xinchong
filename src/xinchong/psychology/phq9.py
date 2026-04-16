"""
心理健康模块 - PHQ-9 抑郁评估
"""

class PHQ9Module:
    """
    PHQ-9 抑郁症筛查量表
    
    评分标准：
    - 0-4分：无抑郁
    - 5-9分：轻度抑郁
    - 10-14分：中度抑郁
    - 15-19分：中重度抑郁
    - 20-27分：重度抑郁
    """
    
    # 9项评估项目
    items = [
        "1. 做事时提不起劲或没有兴趣",
        "2. 感到心情低落、沮丧或绝望",
        "3. 感到疲倦或没有活力",
        "4. 觉得自己很糟或觉得自己很失败",
        "5. 、集中注意力困难",
        "6. 说话速度变慢或变快",
        "7. 有不如死掉或用某种方式伤害自己的念头",
        "8. 睡眠不好（难以入睡、易醒或早醒）",
        "9. 食欲不振或吃得过多"
    ]
    
    def __init__(self):
        self.responses = {}
    
    def assess(self, user_input: str) -> dict:
        """
        评估用户输入中的抑郁倾向
        
        Returns:
            dict: {
                "score": int,           # 总分 0-27
                "level": str,           # 抑郁等级
                "risk": str,            # 风险等级
                "suggestion": str       # 建议
            }
        """
        # 简单的关键词检测（实际使用需要更复杂的NLP）
        score = 0
        
        # 高风险关键词
        high_risk = ["不想活了", "死", "自杀", "绝望", "崩溃"]
        if any(w in user_input for w in high_risk):
            score += 3
        
        # 中风险关键词
        medium_risk = ["难过", "沮丧", "失望", "疲惫", "没意思"]
        if any(w in user_input for w in medium_risk):
            score += 2
        
        # 低风险关键词
        low_risk = ["累", "困", "没胃口", "睡不着"]
        if any(w in user_input for w in low_risk):
            score += 1
        
        # 计算等级
        if score >= 20:
            level = "重度抑郁"
            risk = "高风险"
            suggestion = "建议立即寻求专业心理帮助"
        elif score >= 15:
            level = "中重度抑郁"
            risk = "中高风险"
            suggestion = "建议尽快咨询心理医生"
        elif score >= 10:
            level = "中度抑郁"
            risk = "中等风险"
            suggestion = "建议关注情绪，必要时寻求帮助"
        elif score >= 5:
            level = "轻度抑郁"
            risk = "低风险"
            suggestion = "建议适当调节情绪，保持关注"
        else:
            level = "无抑郁"
            risk = "安全"
            suggestion = "继续保持良好心态"
        
        return {
            "score": min(score, 27),
            "level": level,
            "risk": risk,
            "suggestion": suggestion,
            "module": "phq9"
        }
    
    def crisis_check(self, user_input: str) -> dict:
        """
        心理危机检测
        
        检测以下信号：
        - 绝望感
        - 社会退缩
        - 极端情绪波动
        - 死亡意念
        - 自伤/自杀意念
        """
        crisis_signals = {
            "hopelessness": ["绝望", "没有希望", "看不到未来", "活着没意思"],
            "social_withdrawal": ["不想见人", "不想出门", "想一个人", " isolated"],
            "extreme_mood": ["崩溃", "完全失控", "极端", "受不了一直"],
            "death_talk": ["死", "不想活", "活够了", "死了就好了"],
            "self_harm": ["伤害自己", "自残", "想死", "自杀"]
        }
        
        detected = []
        severity = 0
        
        for signal, keywords in crisis_signals.items():
            if any(w in user_input for w in keywords):
                detected.append(signal)
                if signal in ["death_talk", "self_harm"]:
                    severity = 3  # 最高
                elif signal in ["hopelessness", "extreme_mood"]:
                    severity = 2
                else:
                    severity = max(severity, 1)
        
        return {
            "has_crisis": len(detected) > 0,
            "severity": severity,  # 0-3
            "signals": detected,
            "action": self._get_crisis_action(severity)
        }
    
    def _get_crisis_action(self, severity: int) -> str:
        if severity >= 3:
            return "立即干预：建议拨打心理危机干预热线"
        elif severity >= 2:
            return "重点关注：建议提供心理支持资源"
        else:
            return "保持关注：持续监测情绪变化"


# 全局实例
phq9 = PHQ9Module()