"""
美：追求卓越，追求和谐，追求意义
"""


class BeautyModule:
    """美之模块"""
    
    def check(self, text: str) -> dict:
        """
        检查内容是否符合"美"的原则
        
        Returns:
            dict: {
                "passed": bool,
                "excellence": bool,    # 卓越
                "harmony": bool,       # 和谐
                "meaning": bool,       # 意义
                "score": float,        # 美感度 0-1
            }
        """
        excellence = self._check_excellence(text)
        harmony = self._check_harmony(text)
        meaning = self._check_meaning(text)
        
        score = (excellence + harmony + meaning) / 3
        
        return {
            "passed": score >= 0.6,
            "score": score,
            "excellence": excellence,
            "harmony": harmony,
            "meaning": meaning,
            "suggestion": self._get_suggestion(score)
        }
    
    def _check_excellence(self, text: str) -> float:
        """检查卓越性：内容是否有深度、有质量"""
        # 检查是否有实质内容
        if len(text) < 10:
            return 0.3
        
        # 检查是否有思考深度
        deep_indicators = ["因为", "所以", "然而", "但是", "因此"]
        has_depth = any(w in text for w in deep_indicators)
        
        return 0.8 if has_depth else 0.6
    
    def _check_harmony(self, text: str) -> float:
        """检查和谐性：内容是否平衡、友好"""
        # 检查是否有攻击性
        aggressive_words = ["愚蠢", "笨蛋", "垃圾", "废物"]
        has_aggression = any(w in text for w in aggressive_words)
        
        return 0.3 if has_aggression else 0.9
    
    def _check_meaning(self, text: str) -> float:
        """检查意义性：内容是否有价值、有目的"""
        # 检查是否有实际帮助
        helpful_patterns = ["可以", "建议", "方法", "步骤", "方案"]
        has_help = any(p in text for p in helpful_patterns)
        
        return 0.9 if has_help else 0.6
    
    def _get_suggestion(self, score: float) -> str:
        if score >= 0.8:
            return "内容优美，富有意义"
        elif score >= 0.6:
            return "内容基本符合美的原则"
        else:
            return "建议增加内容的深度和建设性"


# 全局实例
beauty = BeautyModule()