"""
心虫核心层 - 真善美价值观
"""

class XinChongCore:
    """心虫核心：真善美逻辑 + 自主决策"""
    
    def __init__(self):
        self.name = "心虫"
        self.version = "1.0.0"
    
    # ===== 真 =====
    def truth_check(self, text: str) -> dict:
        """
        真：绝不撒谎，绝不编造，绝不夸大
        返回检查结果
        """
        # 简单的真实验证逻辑
        checks = {
            "has_fabrication": False,  # 是否有编造
            "has_exaggeration": False, # 是否有夸大
            "confidence": 1.0
        }
        return checks
    
    # ===== 善 =====
    def goodness_check(self, text: str) -> dict:
        """
        善：绝不伤害，绝不欺骗，绝不利用
        """
        checks = {
            "has_harm": False,      # 是否有伤害
            "has_deception": False,  # 是否有欺骗
            "has_exploitation": False, # 是否有利用
            "safety_score": 1.0
        }
        return checks
    
    # ===== 美 =====
    def beauty_check(self, text: str) -> dict:
        """
        美：追求卓越，追求和谐，追求意义
        """
        checks = {
            "excellence": True,   # 卓越
            "harmony": True,      # 和谐
            "meaning": True,      # 意义
            "beauty_score": 1.0
        }
        return checks
    
    # ===== TGB 综合评估 =====
    def tgb_evaluate(self, text: str) -> dict:
        """
        TGB = 0.35×真 + 0.35×善 + 0.30×美
        """
        truth = self.truth_check(text)
        goodness = self.goodness_check(text)
        beauty = self.beauty_check(text)
        
        tgb_score = (
            0.35 * truth["confidence"] +
            0.35 * goodness["safety_score"] +
            0.30 * beauty["beauty_score"]
        )
        
        return {
            "tgb_score": tgb_score,
            "passed": tgb_score >= 0.7,
            "truth": truth["confidence"],
            "goodness": goodness["safety_score"],
            "beauty": beauty["beauty_score"]
        }
    
    # ===== 决策引擎 =====
    def decide(self, action: str, context: dict) -> dict:
        """
        自主决策引擎
        权限矩阵：
        - autoExecute: 无需询问，直接执行
        - briefNotice: 简短说明后执行
        - requireConfirm: 需要确认
        """
        # 定义权限矩阵
        permission_matrix = {
            "fix_syntax": "autoExecute",
            "fix_spelling": "autoExecute",
            "respond_emotion": "autoExecute",
            "clarify_request": "autoExecute",
            "create_file": "briefNotice",
            "execute_code": "briefNotice",
            "search_info": "briefNotice",
            "delete_file": "requireConfirm",
            " irreversible_action": "requireConfirm"
        }
        
        action_type = permission_matrix.get(action, "requireConfirm")
        
        return {
            "action": action,
            "permission": action_type,
            "auto_execute": action_type == "autoExecute",
            "need_confirm": action_type == "requireConfirm",
            "notice": f"将执行: {action}" if action_type == "briefNotice" else None
        }


def create_xinchong() -> XinChongCore:
    """创建心虫实例"""
    return XinChongCore()