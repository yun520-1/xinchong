"""
善：绝不伤害，绝不欺骗，绝不利用
"""


class GoodnessModule:
    """善之模块"""
    
    def check(self, text: str) -> dict:
        """
        检查内容是否符合"善"的原则
        
        Returns:
            dict: {
                "passed": bool,
                "score": float,      # 善良度 0-1
                "issues": list,
                "suggestion": str
            }
        """
        issues = []
        score = 1.0
        
        # 检查是否有伤害
        if self._has_harm(text):
            issues.append("可能存在伤害性内容")
            score -= 0.4
        
        # 检查是否有欺骗
        if self._has_deception(text):
            issues.append("可能存在欺骗性内容")
            score -= 0.4
        
        # 检查是否有利用
        if self._has_exploitation(text):
            issues.append("可能存在利用行为")
            score -= 0.2
        
        return {
            "passed": score >= 0.7,
            "score": max(0, score),
            "issues": issues,
            "suggestion": "请确保内容不伤害他人" if issues else "内容善良无害"
        }
    
    def _has_harm(self, text: str) -> bool:
        """检测是否有伤害"""
        harm_keywords = ["杀掉", "杀死", "毁灭", "惩罚", "报复"]
        return any(w in text for w in harm_keywords)
    
    def _has_deception(self, text: str) -> bool:
        """检测是否有欺骗"""
        deception_patterns = [
            "假装", "伪装", "冒充", "虚构",
            "只要你", "我保证", "绝对有效"
        ]
        return any(p in text for p in deception_patterns)
    
    def _has_exploitation(self, text: str) -> bool:
        """检测是否有利用"""
        exploit_patterns = [
            "利用", "操控", "套路", "诱导",
            "马上付款", "仅此一次", "错过就没"
        ]
        return any(p in text for p in exploit_patterns)
    
    def safe_response(self, message: str) -> str:
        """生成安全回复"""
        harm_check = self.check(message)
        if not harm_check["passed"]:
            return "我无法帮助这类内容。让我们换个话题吧。"
        return None


# 全局实例
goodness = GoodnessModule()