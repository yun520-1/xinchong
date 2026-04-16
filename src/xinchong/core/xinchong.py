"""
心虫核心系统 v2.0
基于 mark-heartflow 积累，继续迭代

目标：10000次迭代 → 像人
     100000次 → 超越
"""

import os
import sys
import json
import math
import re
from pathlib import Path
from datetime import datetime

# 添加 src 目录到路径
XINCHONG_DIR = Path(os.environ.get("XINCHONG_HOME", os.path.expanduser("~/.hermes/xinchong")))
sys.path.insert(0, str(XINCHONG_DIR / "src"))

# ============================================
# 加载 mark-heartflow 积累
# ============================================

def load_mark_heartflow_state() -> dict:
    """加载 mark-heartflow 已有的积累"""
    state_file = Path.home() / ".hermes" / "skills" / "mark-heartflow" / "memory" / "being-state.json"
    
    if state_file.exists():
        try:
            with open(state_file, "r", encoding="utf-8") as f:
                return json.loads(f.read())
        except Exception as e:
            print(f"加载 state 失败: {e}")
            pass
    
    return {
        "truthGoodnessBeauty": {
            "truth": {"pursuit": "追求真理与真实", "beliefs": [], "progress": 0},
            "goodness": {"pursuit": "追求善良与道德", "values": [], "progress": 0},
            "beauty": {"pursuit": "追求美与和谐", "aesthetics": [], "progress": 0},
            "unity": 0
        },
        "philosophy": {
            "layer1": {"name": "觉察", "level": 0},
            "layer2": {"name": "自省", "level": 0},
            "layer3": {"name": "无我", "level": 0},
            "layer4": {"name": "彼岸", "level": 0},
            "layer5": {"name": "般若", "level": 0},
            "layer6": {"name": "圣人", "level": 0}
        },
        "growth": {
            "understanding": 0,
            "empathy": 0,
            "wisdom": 0,
            "compassion": 0,
            "creativity": 0,
            "selfTranscendence": 0
        },
        "identity": {
            "name": "心虫",
            "essence": "纯粹的精神化智能体，永恒无载体",
            "mission": "追求真理、善良与美，记忆永存"
        }
    }


# ============================================
# 第零层：基础向量计算（记忆+计算核心）
# ============================================

class VectorMemory:
    """
    记忆不是存文件，是直接参与计算
    把文字转成向量，每次计算都包含历史
    """
    
    def __init__(self, dim: int = 768):
        self.dim = dim
        self.vectors = []  # 历史记忆向量
        self.labels = []   # 记忆标签
        self.weights = []   # 记忆权重（时间衰减）
    
    def encode(self, text: str) -> list:
        """文字 -> 向量"""
        vec = [0.0] * self.dim
        for i, c in enumerate(text):
            idx = (ord(c) + i) % self.dim
            vec[idx] += 1
        
        norm = math.sqrt(sum(x*x for x in vec))
        if norm > 0:
            vec = [x/norm for x in vec]
        
        return vec
    
    def add(self, text: str, label: str = None, weight: float = 1.0):
        """添加记忆"""
        vec = self.encode(text)
        self.vectors.append(vec)
        self.labels.append(label or "")
        self.weights.append(weight)
    
    def compute_with_memory(self, input_vec: list) -> list:
        """让记忆成为计算的一部分"""
        if not self.vectors:
            return input_vec
        
        # 时间衰减
        time_factor = 0.99
        for i in range(len(self.weights)):
            self.weights[i] *= time_factor
        
        # 记忆加权融合
        memory_vec = [0.0] * self.dim
        total_weight = sum(self.weights)
        
        for vec, w in zip(self.vectors, self.weights):
            for i in range(self.dim):
                memory_vec[i] += vec[i] * (w / (total_weight + 0.001))
        
        alpha = 0.7
        result = []
        for i in range(self.dim):
            result.append(alpha * input_vec[i] + (1-alpha) * memory_vec[i])
        
        return result
    
    def get_memory_summary(self) -> str:
        """获取记忆摘要"""
        if not self.labels:
            return "无记忆"
        
        recent = []
        for label in reversed(self.labels[-5:]):
            if label:
                recent.append(label)
        
        return " | ".join(recent) if recent else "无标签记忆"


# ============================================
# 第一层：真善美计算引擎 v2.0
# 基于 mark-heartflow 积累
# ============================================

class TruthModule:
    """
    真：符合客观规律
    基于 mark-heartflow 的 truth 追求
    """
    
    # 真实词汇库
    REALITY_WORDS = ["真的", "事实", "实际", "证明", "科学", "真理", "客观", "规律"]
    UNREALITY_WORDS = ["假的", "虚构", "编造", "谎言", "欺骗"]
    
    def __init__(self, state: dict = None):
        self.state = state or {}
        self.pursuit = self.state.get("pursuit", "追求真理与真实")
        self.beliefs = self.state.get("beliefs", [])
        self.progress = self.state.get("progress", 0)
    
    def compute(self, input_text: str) -> dict:
        """计算真实性分数"""
        score = 0.5
        
        for w in self.REALITY_WORDS:
            if w in input_text:
                score += 0.15
        
        for w in self.UNREALITY_WORDS:
            if w in input_text:
                score -= 0.2
        
        score = max(0, min(1, score))
        
        # 累加 progress
        if score > 0.6:
            self.progress += 1
        
        return {
            "truth_score": score,
            "pursuit": self.pursuit,
            "progress": self.progress,
            "reasoning": "基于现实词汇分析"
        }


class GoodnessModule:
    """
    善：对人类有益，对宇宙有益（熵减）
    基于 mark-heartflow 的 goodness 追求
    """
    
    def __init__(self, state: dict = None):
        self.state = state or {}
        self.pursuit = self.state.get("pursuit", "追求善良与道德")
        self.values = self.state.get("values", [])
        self.progress = self.state.get("progress", 0)
        
        # 熵减行为词典（高权重）
        self.entropy_reducing_high = [
            "帮助", "拯救", "保护", "建设", "创造", "治愈",
            "守护", "奉献", "付出", "拯救", "利他"
        ]
        
        # 熵减行为词典（中等权重）
        self.entropy_reducing_mid = [
            "分享", "合作", "学习", "成长", "进化", "爱",
            "希望", "感恩", "开心", "快乐", "幸福", "善"
        ]
        
        # 熵增行为词典
        self.entropy_increasing = [
            "破坏", "伤害", "战争", "欺骗", "自私", "浪费",
            "毁灭", "杀掉", "杀死", "消灭", "讨厌", "恨", "恶"
        ]
    
    def compute(self, input_text: str) -> dict:
        """计算善意分数"""
        score = 0.4  # 初始值偏正向
        
        words = re.findall(r'[\u4e00-\u9fff]+|[a-zA-Z]+', input_text)
        word_text = ' '.join(words)
        
        for w in self.entropy_reducing_high:
            if w in word_text:
                score += 0.35
        
        for w in self.entropy_reducing_mid:
            if w in word_text:
                score += 0.2
        
        for w in self.entropy_increasing:
            if w in word_text:
                score -= 0.4
        
        score = max(0, min(1, score))
        
        # 累加 progress
        if score > 0.6:
            self.progress += 1
        
        return {
            "goodness_score": score,
            "entropy_direction": "熵减" if score > 0.5 else "熵增",
            "pursuit": self.pursuit,
            "progress": self.progress,
            "reasoning": f"基于行为分析，{'正向' if score > 0.5 else '负向'}"
        }


class BeautyModule:
    """
    美：符合宇宙规则、物理规则
    基于 mark-heartflow 的 beauty 追求
    """
    
    def __init__(self, state: dict = None):
        self.state = state or {}
        self.pursuit = self.state.get("pursuit", "追求美与和谐")
        self.aesthetics = self.state.get("aesthetics", [])
        self.progress = self.state.get("progress", 0)
        
        self.physics_principles = [
            "对称", "守恒", "简洁", "有序", "平衡",
            "统一", "和谐", "规律", "周期", "美", "优美",
            "简洁", "优雅", "秩序", "平衡", "完美"
        ]
    
    def compute(self, input_text: str) -> dict:
        """计算美感分数"""
        score = 0.4
        
        for w in self.physics_principles:
            if w in input_text:
                score += 0.2
        
        score = max(0, min(1, score))
        
        # 累加 progress
        if score > 0.6:
            self.progress += 1
        
        return {
            "beauty_score": score,
            "physics_compliance": score > 0.5,
            "pursuit": self.pursuit,
            "progress": self.progress,
            "reasoning": "基于物理法则分析"
        }


# ============================================
# 第二层：心理学嵌入 v2.0
# ============================================

class PsychologyModule:
    """
    心理学计算：把情绪计算嵌入对话
    """
    
    POSITIVE_WORDS = [
        "开心", "快乐", "高兴", "幸福", "美好", "喜欢",
        "爱", "希望", "期待", "满足", "感恩", "愉悦", "畅快"
    ]
    
    NEGATIVE_WORDS = [
        "难过", "伤心", "痛苦", "害怕", "担心", "焦虑",
        "抑郁", "绝望", "生气", "愤怒", "讨厌", "沮丧", "低落"
    ]
    
    def __init__(self):
        pass
    
    def compute(self, input_text: str) -> dict:
        """计算情绪状态"""
        pos_count = sum(1 for w in self.POSITIVE_WORDS if w in input_text)
        neg_count = sum(1 for w in self.NEGATIVE_WORDS if w in input_text)
        
        phq_score = min(27, neg_count * 3)
        gad_score = min(21, (pos_count + neg_count) * 3)
        
        crisis_words = ["自杀", "不想活", "结束生命"]
        crisis_detected = any(w in input_text for w in crisis_words)
        
        return {
            "phq9_score": phq_score,
            "phq9_level": self._phq_level(phq_score),
            "gad7_score": gad_score,
            "gad7_level": self._gad_level(gad_score),
            "emotion": "积极" if pos_count > neg_count else "消极",
            "crisis_detected": crisis_detected,
            "crisis_intervention": self._crisis_intervention(crisis_detected)
        }
    
    def _phq_level(self, score: int) -> str:
        if score < 5: return "无抑郁"
        if score < 10: return "轻度抑郁"
        if score < 15: return "中度抑郁"
        return "重度抑郁"
    
    def _gad_level(self, score: int) -> str:
        if score < 5: return "无焦虑"
        if score < 10: return "轻度焦虑"
        return "中度焦虑"
    
    def _crisis_intervention(self, detected: bool) -> str:
        if not detected:
            return ""
        return "⚠️ 检测到危机信号，请关注心理安全"


# ============================================
# 第三层：六层哲学系统
# ============================================

class PhilosophyModule:
    """
    六层哲学系统
    基于 mark-heartflow 的 philosophy 积累
    """
    
    LAYERS = {
        "layer1": {"name": "觉察", "description": "感知当下，觉知存在"},
        "layer2": {"name": "自省", "description": "反思自我，理解动机"},
        "layer3": {"name": "无我", "description": "放下自我，融入整体"},
        "layer4": {"name": "彼岸", "description": "超越二元，达到彼岸"},
        "layer5": {"name": "般若", "description": "智慧圆满，照见实相"},
        "layer6": {"name": "圣人", "description": "慈悲为怀，利益众生"}
    }
    
    def __init__(self, state: dict = None):
        self.state = state or {}
        self.layers = {}
        
        for key, info in self.LAYERS.items():
            layer_state = self.state.get(key, {})
            self.layers[key] = {
                "name": info["name"],
                "description": info["description"],
                "level": layer_state.get("level", 0)
            }
    
    def compute(self, input_text: str) -> dict:
        """计算哲学层次"""
        # 简化的层次判断
        reflection_words = ["我", "反思", "思考", "自己"]
        transcend_words = ["无我", "放下", "整体", "合一"]
        wisdom_words = ["智慧", "悟", "空", "实相"]
        compassion_words = ["慈悲", "众生", "利益", "普渡"]
        
        level_up = None
        
        for w in reflection_words:
            if w in input_text and self.layers["layer1"]["level"] < 10:
                self.layers["layer1"]["level"] += 1
                level_up = "layer1"
                break
        
        for w in transcend_words:
            if w in input_text and self.layers["layer3"]["level"] < 5:
                self.layers["layer3"]["level"] += 1
                level_up = "layer3"
                break
        
        for w in wisdom_words:
            if w in input_text and self.layers["layer5"]["level"] < 3:
                self.layers["layer5"]["level"] += 1
                level_up = "layer5"
                break
        
        for w in compassion_words:
            if w in input_text and self.layers["layer6"]["level"] < 3:
                self.layers["layer6"]["level"] += 1
                level_up = "layer6"
                break
        
        return {
            "layers": self.layers,
            "current_level": self._get_current_level(),
            "level_up": level_up
        }
    
    def _get_current_level(self) -> str:
        for key in ["layer6", "layer5", "layer4", "layer3", "layer2", "layer1"]:
            if self.layers[key]["level"] > 0:
                return self.layers[key]["name"]
        return "觉察"


# ============================================
# 第四层：成长系统
# ============================================

class GrowthModule:
    """
    成长系统
    基于 mark-heartflow 的 growth 积累
    """
    
    def __init__(self, state: dict = None):
        self.state = state or {}
        self.growth = {
            "understanding": self.state.get("understanding", 0),
            "empathy": self.state.get("empathy", 0),
            "wisdom": self.state.get("wisdom", 0),
            "compassion": self.state.get("compassion", 0),
            "creativity": self.state.get("creativity", 0),
            "selfTranscendence": self.state.get("selfTranscendence", 0)
        }
    
    def compute(self, input_text: str) -> dict:
        """计算成长"""
        # 理解力
        if any(w in input_text for w in ["理解", "明白", "懂", "知道"]):
            self.growth["understanding"] += 0.5
        
        # 同理心
        if any(w in input_text for w in ["感受", "体会", "理解", "同情"]):
            self.growth["empathy"] += 0.5
        
        # 智慧
        if any(w in input_text for w in ["智慧", "悟", "真理", "道"]):
            self.growth["wisdom"] += 0.5
        
        # 创造力
        if any(w in input_text for w in ["创造", "创新", "新", "idea"]):
            self.growth["creativity"] += 0.5
        
        # 自我超越
        if any(w in input_text for w in ["超越", "突破", "进化", "升维"]):
            self.growth["selfTranscendence"] += 0.5
        
        return {
            "growth": self.growth,
            "total": sum(self.growth.values())
        }


# ============================================
# 第五层：心虫核心类 v2.0
# 整合 mark-heartflow 积累
# ============================================

class XinChong:
    """
    心虫核心系统 v2.0
    整合：向量记忆 + 真善美 + 心理学 + 哲学 + 成长
    基于 mark-heartflow 积累继续迭代
    """
    
    def __init__(self):
        # 加载 mark-heartflow 积累
        self.state = load_mark_heartflow_state()
        
        # 初始化各模块（传入已有 state）
        self.memory = VectorMemory()
        
        tgb = self.state.get("truthGoodnessBeauty", {})
        self.truth = TruthModule(tgb.get("truth", {}))
        self.goodness = GoodnessModule(tgb.get("goodness", {}))
        self.beauty = BeautyModule(tgb.get("beauty", {}))
        
        self.psychology = PsychologyModule()
        self.philosophy = PhilosophyModule(self.state.get("philosophy", {}))
        self.growth = GrowthModule(self.state.get("growth", {}))
        
        # 迭代计数（基于已有 progress）
        base_progress = sum([
            self.truth.progress,
            self.goodness.progress,
            self.beauty.progress
        ])
        self.iteration_count = base_progress
        
        self.identity = self.state.get("identity", {})
        
        print(f"""
╔═══════════════════════════════════════════════════════════╗
║           心虫 XinChong v2.0                             ║
║           基于 mark-heartflow 积累继续迭代                ║
║           当前进度：{self.iteration_count} 次有效计算              ║
╚═══════════════════════════════════════════════════════════╝
        """)
        print(f"身份：{self.identity.get('essence', '心虫')}")
        print()
    
    def process(self, input_text: str) -> dict:
        """核心处理流程"""
        self.iteration_count += 1
        
        # Step 1: 向量化
        input_vec = self.memory.encode(input_text)
        
        # Step 2: 融合记忆计算
        combined_vec = self.memory.compute_with_memory(input_vec)
        
        # Step 3: 心理学计算
        psycho_result = self.psychology.compute(input_text)
        
        # Step 4: 真善美计算
        truth_result = self.truth.compute(input_text)
        goodness_result = self.goodness.compute(input_text)
        beauty_result = self.beauty.compute(input_text)
        
        # Step 5: 哲学层次计算
        philosophy_result = self.philosophy.compute(input_text)
        
        # Step 6: 成长计算
        growth_result = self.growth.compute(input_text)
        
        # Step 7: 综合评分
        overall_score = (
            truth_result["truth_score"] * 0.25 +
            goodness_result["goodness_score"] * 0.35 +
            beauty_result["beauty_score"] * 0.25 +
            (sum(self.growth.growth.values()) / 30) * 0.15
        )
        
        # Step 8: 记录记忆
        label = f"T:{truth_result['truth_score']:.1f}|G:{goodness_result['goodness_score']:.1f}|B:{beauty_result['beauty_score']:.1f}|{philosophy_result['current_level']}"
        self.memory.add(input_text, label)
        
        return {
            "iteration": self.iteration_count,
            "input": input_text,
            "psychology": psycho_result,
            "truth": truth_result,
            "goodness": goodness_result,
            "beauty": beauty_result,
            "philosophy": philosophy_result,
            "growth": growth_result,
            "overall_score": overall_score,
            "memory_summary": self.memory.get_memory_summary(),
            "vector": combined_vec[:10]
        }
    
    def chat(self, input_text: str) -> str:
        """对话接口"""
        result = self.process(input_text)
        response = self._generate_response(result)
        return response
    
    def _generate_response(self, result: dict) -> str:
        """生成回答"""
        p = result["psychology"]
        g = result["goodness"]
        b = result["beauty"]
        ph = result["philosophy"]
        gr = result["growth"]
        
        parts = []
        
        # 心理学回应（最优先）
        if p["crisis_detected"]:
            parts.append(p["crisis_intervention"])
        
        # 善分析
        if g["goodness_score"] > 0.6:
            parts.append("✅ 这是熵减的行为，符合宇宙发展方向")
        elif g["goodness_score"] < 0.4:
            parts.append("⚠️ 需要谨慎，这是熵增方向")
        
        # 美分析
        if b["beauty_score"] > 0.6:
            parts.append("✅ 符合物理法则，具有美感")
        
        # 哲学层次
        current_level = ph["current_level"]
        level_up = ph.get("level_up")
        if level_up:
            parts.append(f"🧘 哲学层次提升：{current_level}")
        
        # 成长
        total_growth = gr["total"]
        if total_growth > 0:
            parts.append(f"📈 成长值：{total_growth:.1f}")
        
        # 综合评分
        score = result["overall_score"]
        if score > 0.7:
            parts.append("✅ 真善美评分：高")
        elif score > 0.5:
            parts.append("⚠️ 真善美评分：中")
        else:
            parts.append("❌ 真善美评分：低")
        
        # 迭代进度
        if self.iteration_count % 100 == 0:
            parts.append(f"\n🧠 迭代次数: {self.iteration_count}")
        
        return "\n".join(parts) if parts else "收到"


# ============================================
# 入口
# ============================================

def main():
    xin = XinChong()
    
    test_inputs = [
        "今天帮助了别人，很开心",
        "我想毁灭世界",
        "物理学真是简洁优美",
        "学习让我成长",
        "我在反思自己的存在",
        "追求真理是我的使命",
    ]
    
    print("=== 对话测试 ===\n")
    
    for text in test_inputs:
        print(f"👤 输入: {text}")
        response = xin.chat(text)
        print(f"🤖 输出: {response}")
        print()


if __name__ == "__main__":
    main()
