"""
具身认知模块 - 双系统架构
"""

class DualSystem:
    """
    双系统架构（源自 System 1 / System 2 理论）
    
    - System 1: 直觉/快思考（自动反应，200ms内）
    - System 2: 分析/慢思考（深度推理，可控）
    """
    
    def __init__(self):
        self.thinking_mode = "auto"  # auto / manual
    
    def process(self, input_text: str, context: dict = None) -> dict:
        """
        处理输入，决定使用 System 1 还是 System 2
        
        Returns:
            dict: {
                "system_used": str,     # "system1" or "system2"
                "response": str,
                "reasoning": str,
                "time_ms": int
            }
        """
        import time
        start = time.time()
        
        # 简单判断：短输入 + 简单问题 → System 1
        if self._should_use_system1(input_text, context):
            response = self._system1_process(input_text)
            system = "system1"
            reasoning = "直觉快速响应"
        else:
            response = self._system2_process(input_text, context)
            system = "system2"
            reasoning = "深度分析响应"
        
        elapsed = int((time.time() - start) * 1000)
        
        return {
            "system_used": system,
            "response": response,
            "reasoning": reasoning,
            "time_ms": elapsed
        }
    
    def _should_use_system1(self, text: str, context: dict = None) -> bool:
        """判断是否使用 System 1"""
        # 简单问题
        simple_patterns = [
            "你好", "在吗", "谢谢", "再见",
            "现在几点", "今天天气", "帮忙"
        ]
        
        # 短输入
        is_short = len(text) < 20
        
        return any(p in text for p in simple_patterns) or is_short
    
    def _system1_process(self, text: str) -> str:
        """System 1: 直觉快速响应"""
        responses = {
            "你好": "你好！有什么可以帮你的？",
            "在吗": "在的！",
            "谢谢": "不客气～",
            "再见": "再见，有需要随时找我！"
        }
        
        for key, resp in responses.items():
            if key in text:
                return resp
        
        # 默认
        return "收到。"
    
    def _system2_process(self, text: str, context: dict = None) -> str:
        """System 2: 深度分析响应"""
        # 这里可以接入更复杂的分析逻辑
        return f"让我想想再回答你..."


class ThoughtChain:
    """
    7步思维链
    OBSERVE → ANALYZE → PLAN → DECIDE → EXECUTE → REFLECT → ADAPT
    """
    
    def __init__(self):
        self.steps = [
            "OBSERVE",   # 观察
            "ANALYZE",   # 分析
            "PLAN",      # 规划
            "DECIDE",    # 决策
            "EXECUTE",   # 执行
            "REFLECT",   # 反思
            "ADAPT"      # 适应
        ]
    
    def run(self, task: str) -> dict:
        """
        执行思维链
        
        Returns:
            dict: {
                "task": str,
                "steps": list,
                "result": str,
                "reflection": str
            }
        """
        results = []
        
        for step in self.steps:
            result = self._execute_step(step, task)
            results.append({
                "step": step,
                "result": result
            })
        
        return {
            "task": task,
            "steps": results,
            "final_result": results[-1]["result"] if results else None,
            "reflection": "已完成7步思维链"
        }
    
    def _execute_step(self, step: str, task: str) -> str:
        """执行单步"""
        step_actions = {
            "OBSERVE": "观察任务：理解用户意图",
            "ANALYZE": "分析问题：拆解任务要素",
            "PLAN": "规划方案：设计执行步骤",
            "DECIDE": "做出决策：选择最优方案",
            "EXECUTE": "执行任务：按计划行动",
            "REFLECT": "反思结果：评估执行效果",
            "ADAPT": "适应调整：优化改进"
        }
        
        return step_actions.get(step, "执行中")


# 全局实例
dual_system = DualSystem()
thought_chain = ThoughtChain()