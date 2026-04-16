"""
真：绝不撒谎，绝不编造，绝不夸大
"""


class TruthModule:
    """真之模块"""
    
    def check(self, text: str) -> dict:
        """
        检查内容是否符合"真"的原则
        
        Returns:
            dict: {
                "passed": bool,      # 是否通过
                "score": float,      # 真实度 0-1
                "issues": list,      # 发现的问题
                "suggestion": str    # 改进建议
            }
        """
        issues = []
        score = 1.0
        
        # 检查是否有编造事实的迹象
        if self._has_fabrication(text):
            issues.append("可能存在编造内容")
            score -= 0.3
        
        # 检查是否有夸大
        if self._has_exaggeration(text):
            issues.append("可能存在夸大")
            score -= 0.2
        
        # 检查是否有不确定的内容声称确定
        if self._has_false_certainty(text):
            issues.append("不确定的内容被确定化")
            score -= 0.2
        
        return {
            "passed": score >= 0.7,
            "score": max(0, score),
            "issues": issues,
            "suggestion": "请确保所有信息基于事实" if issues else "内容真实可靠"
        }
    
    def _has_fabrication(self, text: str) -> bool:
        """检测是否有编造"""
        # 简单检测：包含无法验证的详细细节
        fabrication_patterns = [
            "具体来说", "根据调查显示", "权威数据表明",
            "据XX机构研究", "专家称"
        ]
        return any(p in text for p in fabrication_patterns)
    
    def _has_exaggeration(self, text: str) -> bool:
        """检测是否有夸大"""
        exaggeration_words = ["最", "绝对", "完美", "无敌", "第一"]
        return any(w in text for w in exaggeration_words)
    
    def _has_false_certainty(self, text: str) -> bool:
        """检测不确定内容被确定化"""
        uncertain_phrases = ["可能是", "可能是", "应该"]
        certain_phrases = ["就是", "肯定是", "一定是"]
        
        has_uncertain = any(p in text for p in uncertain_phrases)
        has_certain = any(p in text for p in certain_phrases)
        
        return has_uncertain and has_certain
    
    def honest_response(self, message: str) -> str:
        """生成诚实回复"""
        if "不知道" in message or "怎么做" in message:
            return "我需要更多信息才能准确回答。你能具体说明一下你的需求吗？"
        return None


# 全局实例
truth = TruthModule()