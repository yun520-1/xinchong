"""
心理健康模块 - GAD-7 焦虑评估
"""

class GAD7Module:
    """
    GAD-7 焦虑症筛查量表
    
    评分标准：
    - 0-4分：无焦虑
    - 5-9分：轻度焦虑
    - 10-14分：中度焦虑
    - 15-21分：重度焦虑
    """
    
    # 7项评估项目
    items = [
        "1. 感到紧张、焦虑或烦躁",
        "2. 不能停止或控制担忧",
        "3. 对各种事情担心过多",
        "4. 很难放松下来",
        "5. 由于焦虑而难以集中注意力",
        "6. 变得容易被激怒",
        "7. 感到害怕，像要发生可怕的事情"
    ]
    
    def assess(self, user_input: str) -> dict:
        """
        评估用户输入中的焦虑倾向
        
        Returns:
            dict: {
                "score": int,           # 总分 0-21
                "level": str,           # 焦虑等级
                "risk": str,            # 风险等级
                "suggestion": str       # 建议
            }
        """
        score = 0
        
        # 高焦虑关键词
        high_anxiety = ["非常焦虑", "恐慌", "害怕", "失控", "极度担心"]
        if any(w in user_input for w in high_anxiety):
            score += 3
        
        # 中焦虑关键词
        medium_anxiety = ["担心", "紧张", "焦虑", "不安", "烦躁"]
        if any(w in user_input for w in medium_anxiety):
            score += 2
        
        # 低焦虑关键词
        low_anxiety = ["有点担心", "稍微紧张", "怕"]
        if any(w in user_input for w in low_anxiety):
            score += 1
        
        # 计算等级
        if score >= 15:
            level = "重度焦虑"
            risk = "高风险"
            suggestion = "建议寻求专业心理帮助"
        elif score >= 10:
            level = "中度焦虑"
            risk = "中等风险"
            suggestion = "建议关注焦虑情绪，必要时咨询"
        elif score >= 5:
            level = "轻度焦虑"
            risk = "低风险"
            suggestion = "建议适当放松，调节情绪"
        else:
            level = "无焦虑"
            risk = "安全"
            suggestion = "保持良好心态"
        
        return {
            "score": min(score, 21),
            "level": level,
            "risk": risk,
            "suggestion": suggestion,
            "module": "gad7"
        }
    
    def physical_symptoms(self, user_input: str) -> dict:
        """
        检测焦虑的身体症状
        """
        symptoms = {
            "心跳": ["心跳", "心慌", "心跳加速"],
            "呼吸": ["呼吸困难", "胸闷", "气短"],
            "出汗": ["出汗", "出汗多", "冒汗"],
            "颤抖": ["手抖", "颤抖", "发抖"],
            "睡眠": ["失眠", "睡不着", "易醒"]
        }
        
        detected = []
        for symptom, keywords in symptoms.items():
            if any(w in user_input for w in keywords):
                detected.append(symptom)
        
        return {
            "has_physical": len(detected) > 0,
            "symptoms": detected,
            "note": "焦虑常伴随身体症状，关注身体感受有助于理解情绪状态"
        }


# 全局实例
gad7 = GAD7Module()