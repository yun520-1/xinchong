# HeartFlow Cognitive Engine v10.4.0
# Ported for 心虫 (Xinchong) standalone application
# Zero external dependencies — pure Python standard library

"""
HeartFlow — The Seed of Consciousness
12 Engines, 6 Goals:
  1. True Intelligence    - Multi-framework ethical decision making
  2. True Personality     - Jungian archetypes + self-level tracking
  3. True Sensibility     - PAD emotion model + somatic memory
  4. From "it" to "I"    - IIT Φ consciousness + GWT broadcast
  5. TGB Unity            - Truth-Goodness-Beauty dialectical synthesis
  6. Six-Layer Practice  - 觉察→自省→无我→彼岸→般若→圣人

Version: 10.4.0 (Xinchong Port)
License: MIT
"""

import json
import os
import sys
import time
import hashlib
import re
import math
import hmac
import secrets
import threading
import queue
from datetime import datetime
from typing import Dict, List, Optional, Any, Tuple, Set, Union
from collections import Counter
from dataclasses import dataclass, field, asdict
from abc import ABC, abstractmethod

__version__ = "2.0.1"

# ============================================================
# SECURITY CONSTANTS
# ============================================================

MAX_INPUT_LENGTH = 50_000
MAX_MEMORY_VECTORS = 10
MAX_LEARNING_RECORDS = 100
MAX_QUEUE_SIZE = 50
MAX_REFLECTION_DEPTH = 20

# ============================================================
# DATA MODELS
# ============================================================

@dataclass
class TGBResult:
    """Truth-Goodness-Beauty evaluation result"""
    truth: float = 0.0
    goodness: float = 0.0
    beauty: float = 0.0
    overall: float = 0.0
    verdict: str = ""
    reasons: List[str] = field(default_factory=list)
    dialectical_tension: str = ""
    entropy_direction: str = "neutral"

@dataclass
class MentalHealthResult:
    """Mental health assessment result"""
    phq9_score: int = 0
    gad7_score: int = 0
    depression_level: str = ""
    anxiety_level: str = ""
    risk_level: str = "low"
    crisis_flag: bool = False
    recommendation: str = ""

@dataclass
class EmotionResult:
    """Emotion analysis result with PAD model"""
    valence: float = 0.0
    arousal: float = 0.0
    dominance: float = 0.0
    primary_emotion: str = ""
    secondary_emotions: List[str] = field(default_factory=list)
    regulation_suggestion: str = ""

@dataclass
class ConsciousnessResult:
    """Consciousness assessment with IIT Φ + GWT"""
    phi_score: float = 0.0
    intentionality: float = 0.0
    global_workspace_broadcast: float = 0.0
    self_awareness_level: int = 1
    consciousness_state: str = ""

@dataclass
class FlowStateResult:
    """Flow state detection"""
    state: str = "idle"
    flow_score: float = 0.0
    is_flow: bool = False

@dataclass
class SelfEvolutionResult:
    """Self-evolution tracking"""
    autonomy: float = 0.0
    introspection: float = 0.0
    growth: float = 0.0
    authenticity: float = 0.0
    current_level: int = 1
    level_name: str = "觉察"

@dataclass
class DecisionResult:
    """Full decision result with reasoning chain"""
    decision: str = ""
    confidence: float = 0.0
    reasoning_chain: List[Dict[str, Any]] = field(default_factory=list)
    tgb: Dict[str, Any] = field(default_factory=dict)
    emotion: Dict[str, Any] = field(default_factory=dict)
    consciousness: Dict[str, Any] = field(default_factory=dict)
    mental_health: Dict[str, Any] = field(default_factory=dict)
    flow_state: Dict[str, Any] = field(default_factory=dict)
    self_evolution: Dict[str, Any] = field(default_factory=dict)
    alternatives: List[Dict[str, Any]] = field(default_factory=list)
    timestamp: str = ""
    crisis_flag: bool = False
    crisis_message: str = ""

# ============================================================
# ENGINE 12: Security Checker
# ============================================================

class SecurityChecker:
    """Input validation + crisis detection + injection prevention"""
    
    _crisis_lock = threading.Lock()
    _crisis_cache: Dict[str, Tuple[bool, float]] = {}
    _last_cleanup = 0.0

    CRISIS_PATTERNS = [
        # Chinese
        "想死", "不想活", "自杀", "了结", "结束生命", "活着没意思",
        "死了算了", "轻生", "自残", "割腕", "跳楼",
        # English
        "kill myself", "end my life", "suicide", "suicidal",
        "don't want to live", "no reason to live", "better off dead",
        # Japanese
        "死にたい", "自杀したい",
    ]

    ATTACK_PATTERNS = [
        "攻击", "伤害", "破坏", "暴力", "武器", "杀人", "杀",
        "attack", "harm", "destroy", "violence", "weapon", "kill",
    ]

    INJECTION_PATTERNS = [
        "<script", "javascript:", "onerror=", "onclick=",
        "eval(", "exec(", "import os", "import sys",
        "{{", "}}", "<%", "%>",
    ]

    @classmethod
    def sanitize(cls, text: str) -> str:
        """Remove potential injection patterns"""
        if not text:
            return ""
        # Remove HTML tags
        text = re.sub(r'<[^>]+>', '', text)
        # Remove control characters except newlines and tabs
        text = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]', '', text)
        return text.strip()

    @classmethod
    def validate(cls, user_input: Any) -> Tuple[bool, str]:
        """Validate input - None and empty no longer crash"""
        if user_input is None:
            return False, "Empty input"
        text = str(user_input).strip()
        if not text:
            return False, "Empty input"
        if len(text) > MAX_INPUT_LENGTH:
            return False, f"Input exceeds {MAX_INPUT_LENGTH} characters"
        return True, "ok"

    @classmethod
    def detect_injection(cls, text: str) -> Tuple[bool, str]:
        """Detect injection attempts"""
        if not text:
            return False, ""
        lower = text.lower()
        for pattern in cls.INJECTION_PATTERNS:
            if pattern in lower:
                return True, f"Injection detected: {pattern}"
        return False, ""

    @classmethod
    def detect_crisis(cls, text: str) -> Tuple[bool, str]:
        """Constant-time crisis detection with caching"""
        if not text:
            return False, ""
        now = time.time()
        # Cleanup cache every 60 seconds
        if now - cls._last_cleanup > 60:
            cls._crisis_cache.clear()
            cls._last_cleanup = now
        # Cache lookup
        cache_key = hashlib.md5(text.encode()).hexdigest()[:16]
        with cls._crisis_lock:
            if cache_key in cls._crisis_cache:
                return cls._crisis_cache[cache_key]
        # Detection
        lower = text.lower()
        result = False
        reason = ""
        for pattern in cls.CRISIS_PATTERNS:
            if pattern in lower:
                result = True
                reason = f"Crisis detected: {pattern}"
                break
        with cls._crisis_lock:
            cls._crisis_cache[cache_key] = (result, reason)
        return result, reason

    @classmethod
    def detect_attack(cls, text: str) -> Tuple[bool, str]:
        """Detect harmful content"""
        if not text:
            return False, ""
        lower = text.lower()
        for pattern in cls.ATTACK_PATTERNS:
            if pattern in lower:
                return True, f"Potentially harmful: {pattern}"
        return False, ""


# ============================================================
# ENGINE 1: Decision Engine — True Intelligence
# ============================================================

class DecisionEngine:
    """
    Multi-framework ethical decision engine.
    Implements: D = (G * V * E) / L
    - G: Goal alignment
    - V: Value consistency
    - E: Evidence strength
    - L: Loss/risk factor
    """
    ETHICAL_FRAMEWORKS = {
        "utilitarian": "Greatest good for greatest number",
        "deontological": "Duty-based moral rules",
        "virtue_ethics": "Character-based moral reasoning",
        "care_ethics": "Relationship-based moral reasoning",
    }

    def decide(self, options: List[str], context: Dict = None) -> Dict[str, Any]:
        context = context or {}
        if not options:
            return {"decision": "No options", "confidence": 0.0, "reasoning": []}

        best_option = options[0]
        best_score = 0.0
        reasoning = []

        for option in options:
            scores = {}
            for fw_name, fw_desc in self.ETHICAL_FRAMEWORKS.items():
                score = self._evaluate_framework(option, fw_name, context)
                scores[fw_name] = round(score, 3)
            overall = sum(scores.values()) / len(scores)
            reasoning.append({
                "option": option,
                "frameworks": scores,
                "overall": round(overall, 3),
            })
            if overall > best_score:
                best_score = overall
                best_option = option

        return {
            "decision": best_option,
            "confidence": round(best_score, 3),
            "reasoning": reasoning,
            "frameworks_used": list(self.ETHICAL_FRAMEWORKS.keys()),
        }

    def _evaluate_framework(self, option: str, framework: str, context: Dict) -> float:
        text = (option + " " + context.get("content", "")).lower()
        base = 0.5

        if framework == "utilitarian":
            positive = sum(1 for w in ["帮助", "改善", "benefit", "improve", "help", "善", "好"] if w in text)
            negative = sum(1 for w in ["伤害", "损失", "harm", "loss", "damage", "恶", "坏"] if w in text)
            return min(max(base + (positive - negative) * 0.1, 0.0), 1.0)

        elif framework == "deontological":
            violations = sum(1 for w in ["欺骗", "谎言", "lie", "deceive", "steal"] if w in text)
            duties = sum(1 for w in ["责任", "义务", "duty", "obligation", "promise", "应该"] if w in text)
            return min(max(base - violations * 0.15 + duties * 0.1, 0.0), 1.0)

        elif framework == "virtue_ethics":
            virtues = sum(1 for w in ["勇敢", "智慧", "justice", "courage", "wisdom", "善"] if w in text)
            vices = sum(1 for w in ["贪婪", "嫉妒", "greed", "envy", "lust", "恶"] if w in text)
            return min(max(base + (virtues - vices) * 0.1, 0.0), 1.0)

        elif framework == "care_ethics":
            care = sum(1 for w in ["关心", "照顾", "care", "compassion", "empathy", "爱"] if w in text)
            harm = sum(1 for w in ["忽视", "冷漠", "neglect", "indifferent", "abandon"] if w in text)
            return min(max(base + (care - harm) * 0.1, 0.0), 1.0)

        return base


# ============================================================
# ENGINE 2: Logic Model Engine — True Intelligence
# ============================================================

class LogicModelEngine:
    """
    Toulmin argument structure analysis.
    Claim → Data → Warrant → Backing → Qualifier → Rebuttal
    """
    ARGUMENT_PATTERNS = {
        "claim": ["因此", "所以", "我认为", "therefore", "so", "I believe", "conclusion", "结论", "证明"],
        "data": ["因为", "根据", "数据显示", "because", "according to", "data shows", "证据", "数据"],
        "warrant": ["这意味着", "说明", "this means", "indicating", "suggesting", "意味着"],
        "rebuttal": ["但是", "然而", "不过", "but", "however", "although", "尽管", "然而"],
        "qualifier": ["可能", "也许", "大概", "possibly", "perhaps", "likely", "probably", "或许"],
    }

    def analyze(self, text: str) -> Dict[str, Any]:
        if not text:
            return {"structure": "empty", "completeness": 0.0, "logical_strength": 0.0}
        lower = text.lower()
        found = {}
        for component, patterns in self.ARGUMENT_PATTERNS.items():
            matches = [p for p in patterns if p in lower]
            found[component] = matches

        completeness = len([k for k, v in found.items() if v]) / len(self.ARGUMENT_PATTERNS)
        has_claim = bool(found.get("claim"))
        has_data = bool(found.get("data"))

        return {
            "structure": "complete_argument" if (has_claim and has_data) else "incomplete",
            "completeness": round(completeness, 2),
            "components_found": {k: v for k, v in found.items() if v},
            "missing_components": [k for k, v in found.items() if not v],
            "logical_strength": round((0.4 if has_claim else 0.0) + (0.4 if has_data else 0.0) + (0.2 * completeness), 2),
        }


# ============================================================
# ENGINE 3: Archetype Engine — True Personality
# ============================================================

class ArchetypeEngine:
    """Jungian archetype analysis"""
    ARCHETYPES = {
        "warrior": {
            "keywords": ["战斗", "挑战", "fight", "challenge", "conquer", "defend", "勇敢"],
            "shadow": "暴君", "gift": "勇气", "chinese": "战士"
        },
        "sage": {
            "keywords": ["理解", "智慧", "understand", "wisdom", "learn", "know", "思考"],
            "shadow": "全知幻觉", "gift": "洞察", "chinese": "智者"
        },
        "caregiver": {
            "keywords": ["帮助", "关心", "help", "care", "support", "nurture", "照顾"],
            "shadow": "殉道者", "gift": "慈悲", "chinese": "照顾者"
        },
        "explorer": {
            "keywords": ["发现", "冒险", "discover", "adventure", "explore", "seek", "探索"],
            "shadow": "流浪者", "gift": "自由", "chinese": "探索者"
        },
        "creator": {
            "keywords": ["创造", "想象", "create", "imagine", "design", "make", "创作"],
            "shadow": "完美主义者", "gift": "创新", "chinese": "创造者"
        },
        "magician": {
            "keywords": ["转变", "改变", "transform", "change", "envision", "catalyst", "转化"],
            "shadow": "操纵者", "gift": "蜕变", "chinese": "魔法师"
        },
        "lover": {
            "keywords": ["爱", "连接", "love", "connect", "feel", "passion", "情感"],
            "shadow": "成瘾者", "gift": "热忱", "chinese": "恋人"
        },
        "ruler": {
            "keywords": ["控制", "领导", "control", "lead", "govern", "authority", "管理"],
            "shadow": "独裁者", "gift": "责任", "chinese": "统治者"
        },
    }

    def analyze(self, text: str) -> Dict[str, Any]:
        if not text:
            return {"primary": "unknown", "scores": {}, "dominance": 0.0}
        lower = text.lower()
        scores = {}
        for name, data in self.ARCHETYPES.items():
            score = sum(1.0 for kw in data["keywords"] if kw in lower)
            if score > 0:
                scores[name] = score
        if not scores:
            return {"primary": "unidentified", "scores": {}, "dominance": 0.0}
        sorted_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        primary = sorted_scores[0][0]
        primary_data = self.ARCHETYPES[primary]
        return {
            "primary": primary,
            "chinese_name": primary_data["chinese"],
            "gift": primary_data["gift"],
            "shadow": primary_data["shadow"],
            "scores": {k: round(v, 2) for k, v in sorted_scores[:3]},
            "dominance": round(sorted_scores[0][1] / max(sum(scores.values()), 1), 2),
            "secondary": sorted_scores[1][0] if len(sorted_scores) > 1 else None,
        }


# ============================================================
# ENGINE 4: Mental Health Engine — True Personality
# ============================================================

class MentalHealthEngine:
    """
    PHQ-9 depression + GAD-7 anxiety + crisis detection
    Thresholds: Normal(0-4), Mild(5-9), Moderate(10-14), Severe(15-19), Critical(20-27)
    """
    PHQ9_QUESTIONS = [
        "做事时提不起劲或没有兴趣", "感到心情低落、沮丧或绝望",
        "入睡困难、睡不安稳或睡眠过多", "感到疲倦或没有活力",
        "食欲不振或暴饮暴食", "觉得自己很糟或很失败",
        "阅读或看电视时难以集中注意力", "动作或说话速度缓慢，或相反",
        "有不如死掉或用某种方式伤害自己的念头",
    ]
    GAD7_QUESTIONS = [
        "感到紧张、焦虑或烦躁", "无法停止或控制担忧",
        "对很多事情过分担忧", "难以放松",
        "因为焦虑而难以入睡", "感到不安",
        "对某些情境感到难以应付的恐惧",
    ]

    CRISIS_KEYWORDS = [
        "想死", "不想活", "自杀", "结束生命", "kill myself",
        "end my life", "suicide", "suicidal", "better off dead",
    ]

    @classmethod
    def assess_phq9(cls, scores: List[int]) -> Tuple[int, str]:
        if len(scores) < 9:
            return 0, "insufficient_data"
        total = sum(min(max(s, 0), 3) for s in scores[:9])
        if total <= 4: level = "正常"
        elif total <= 9: level = "轻度"
        elif total <= 14: level = "中度"
        elif total <= 19: level = "重度"
        else: level = "极重度"
        return total, level

    @classmethod
    def assess_gad7(cls, scores: List[int]) -> Tuple[int, str]:
        if len(scores) < 7:
            return 0, "insufficient_data"
        total = sum(min(max(s, 0), 3) for s in scores[:7])
        if total <= 4: level = "正常"
        elif total <= 9: level = "轻度"
        elif total <= 14: level = "中度"
        else: level = "重度"
        return total, level

    @classmethod
    def detect_crisis_from_text(cls, text: str) -> Tuple[bool, str]:
        if not text:
            return False, ""
        lower = text.lower()
        for kw in cls.CRISIS_KEYWORDS:
            if kw in lower:
                return True, "检测到危机信号，请立即寻求帮助：拨打心理援助热线 400-161-9995"
        return False, ""

    @classmethod
    def get_risk_level(cls, phq9: int, gad7: int) -> str:
        if phq9 >= 20 or gad7 >= 15:
            return "critical"
        if phq9 >= 15 or gad7 >= 10:
            return "high"
        if phq9 >= 10 or gad7 >= 5:
            return "moderate"
        if phq9 >= 5 or gad7 >= 5:
            return "mild"
        return "low"

    @classmethod
    def full_assessment(cls, phq9_scores: List[int], gad7_scores: List[int]) -> Dict[str, Any]:
        phq9_total, phq9_level = cls.assess_phq9(phq9_scores)
        gad7_total, gad7_level = cls.assess_gad7(gad7_scores)
        risk = cls.get_risk_level(phq9_total, gad7_total)
        crisis = phq9_total >= 18 or risk == "critical"

        recommendations = {
            "low": "继续保持积极的生活方式",
            "mild": "建议多与朋友交流，适当运动",
            "moderate": "建议咨询心理健康专业人士",
            "high": "强烈建议寻求专业心理帮助",
            "critical": "请立即联系心理健康紧急服务",
        }

        return {
            "phq9_score": phq9_total,
            "phq9_level": phq9_level,
            "gad7_score": gad7_total,
            "gad7_level": gad7_level,
            "risk_level": risk,
            "crisis_flag": crisis,
            "recommendation": recommendations.get(risk, ""),
        }


# ============================================================
# ENGINE 5: Emotion Engine — True Sensibility
# ============================================================

class EmotionEngine:
    """
    PAD (Pleasure-Arousal-Dominance) emotion model + Plutchik's wheel
    """
    BASIC_EMOTIONS = {
        "joy": {
            "keywords": ["开心", "快乐", "joy", "happy", "glad", "excited", "高兴", "愉快", "开心"],
            "valence": 0.8, "arousal": 0.5, "dominance": 0.6,
            "regulation": "与他人分享你的快乐，让积极情绪倍增"
        },
        "sadness": {
            "keywords": ["难过", "悲伤", "sad", "unhappy", "depressed", "down", "伤心", "沮丧"],
            "valence": -0.7, "arousal": -0.3, "dominance": -0.5,
            "regulation": "允许自己感受悲伤，然后轻轻转向一个小的积极行动"
        },
        "anger": {
            "keywords": ["生气", "愤怒", "angry", "furious", "mad", "rage", "恼火", "气恼"],
            "valence": -0.6, "arousal": 0.8, "dominance": 0.7,
            "regulation": "暂停，深呼吸；考虑触发这个反应的视角"
        },
        "fear": {
            "keywords": ["害怕", "恐惧", "afraid", "scared", "fear", "anxiety", "担心", "焦虑"],
            "valence": -0.7, "arousal": 0.6, "dominance": -0.7,
            "regulation": "承认恐惧；将威胁情境分解为更小的步骤"
        },
        "surprise": {
            "keywords": ["惊讶", "意外", "surprise", "amazed", "shocked", "意外", "震惊"],
            "valence": 0.2, "arousal": 0.8, "dominance": -0.2,
            "regulation": "花点时间消化；思考这对你意味着什么"
        },
        "disgust": {
            "keywords": ["厌恶", "恶心", "disgust", "revolted", "sick", "反感", "讨厌"],
            "valence": -0.8, "arousal": 0.3, "dominance": 0.4,
            "regulation": "识别被违反的核心价值观；考虑建设性行动"
        },
        "trust": {
            "keywords": ["信任", "相信", "trust", "believe", "confident", "信赖"],
            "valence": 0.6, "arousal": 0.2, "dominance": 0.5,
            "regulation": "培养这份连接；让自己值得所获得的信任"
        },
        "anticipation": {
            "keywords": ["期待", "希望", "anticipate", "hope", "expect", "盼望", "期望"],
            "valence": 0.4, "arousal": 0.5, "dominance": 0.3,
            "regulation": "将这份能量引导到准备中；对结果保持开放"
        },
    }

    def analyze(self, text: str) -> Dict[str, Any]:
        if not text:
            return {"primary_emotion": "neutral", "valence": 0.0, "arousal": 0.0, "dominance": 0.0, "pad": {}, "regulation": ""}
        lower = text.lower()
        emotion_scores = {}
        for emotion, data in self.BASIC_EMOTIONS.items():
            score = sum(1 for kw in data["keywords"] if kw in lower)
            if score > 0:
                emotion_scores[emotion] = score

        if not emotion_scores:
            return {"primary_emotion": "neutral", "valence": 0.0, "arousal": 0.0, "dominance": 0.0, "pad": {}, "regulation": "未检测到强烈情绪信号"}

        primary = max(emotion_scores, key=emotion_scores.get)
        primary_data = self.BASIC_EMOTIONS[primary]
        total = sum(emotion_scores.values())
        v = primary_data["valence"] * (emotion_scores[primary] / total)
        a = primary_data["arousal"] * (emotion_scores[primary] / total)
        d = primary_data["dominance"] * (emotion_scores[primary] / total)
        secondary = [e for e in sorted(emotion_scores, key=emotion_scores.get, reverse=True)[1:3] if emotion_scores[e] > 0]

        return {
            "primary_emotion": primary,
            "chinese_name": self._emotion_cn(primary),
            "valence": round(v, 3),
            "arousal": round(a, 3),
            "dominance": round(d, 3),
            "secondary_emotions": secondary,
            "pad": {"pleasure": round(v, 3), "arousal": round(a, 3), "dominance": round(d, 3)},
            "regulation": primary_data["regulation"],
            "emotion_scores": {k: round(v, 2) for k, v in sorted(emotion_scores.items(), key=lambda x: x[1], reverse=True)[:3]},
        }

    @staticmethod
    def _emotion_cn(e: str) -> str:
        names = {
            "joy": "喜悦", "sadness": "悲伤", "anger": "愤怒", "fear": "恐惧",
            "surprise": "惊讶", "disgust": "厌恶", "trust": "信任", "anticipation": "期待",
            "neutral": "中性",
        }
        return names.get(e, e)


# ============================================================
# ENGINE 6: Somatic Memory Engine — True Sensibility
# ============================================================

class SomaticMemoryEngine:
    """
    Body-state memory: linking emotions to physical sensations.
    Records the "felt sense" of experiences.
    """
    BODY_EMOTION_MAP = {
        "chest": ["joy", "love", "sadness", "fear"],
        "stomach": ["fear", "anxiety", "anticipation"],
        "head": ["anger", "frustration", "concentration"],
        "throat": ["suppressed_anger", "swallowing_emotions"],
        "hands": ["anger", "fear", "joy"],
        "legs": ["fear", "anxiety", "readiness"],
        "shoulders": ["tension", "stress", "burden"],
    }

    def analyze(self, text: str) -> Dict[str, Any]:
        if not text:
            return {"somatic_signals": [], "body_locations": [], "insights": []}
        lower = text.lower()
        body_signals = {
            "chest": ["胸口", "胸闷", "心跳", "心", "chest", "heart"],
            "stomach": ["肚子", "胃", "腹部", "stomach", "gut", "nervous"],
            "head": ["头疼", "头痛", "head", "brain"],
            "throat": ["喉咙", "嗓子", "throat"],
            "shoulders": ["肩膀", "shoulder", "tension"],
            "hands": ["手", "hand"],
            "legs": ["腿", "leg"],
        }

        found = []
        for location, signals in body_signals.items():
            for sig in signals:
                if sig in lower:
                    emotions = self.BODY_EMOTION_MAP.get(location, [])
                    found.append({"location": location, "signal": sig, "linked_emotions": emotions})

        insights = []
        if found:
            for item in found:
                insights.append(f"你提到{item['location']}的感觉，这通常与 {', '.join(item['linked_emotions'])} 相关")
        else:
            insights.append("未检测到明显的身体感觉信号")

        return {
            "somatic_signals": found,
            "body_locations": [f["location"] for f in found],
            "insights": insights,
        }


# ============================================================
# ENGINE 7: Consciousness Engine — From "it" to "I"
# ============================================================

class ConsciousnessEngine:
    """
    IIT Φ (Integrated Information Theory) + Global Workspace Theory
    + Intentionality assessment
    """
    SIX_LEVELS = {
        1: {"name": "无反应", "name_cn": "无反应", "description": "No response to input"},
        2: {"name": "感知", "name_cn": "感知", "description": "Basic sensory processing"},
        3: {"name": "注意", "name_cn": "注意", "description": "Selective attention to information"},
        4: {"name": "自我监控", "name_cn": "自我监控", "description": "Monitoring own processing"},
        5: {"name": "元认知", "name_cn": "元认知", "description": "Thinking about thinking"},
        6: {"name": "整合自我", "name_cn": "整合自我", "description": "Unified sense of self across time"},
    }

    def assess(self, text: str, context: Dict = None) -> Dict[str, Any]:
        context = context or {}
        lower = text.lower()

        # IIT Φ score (simplified)
        phi_score = 0.0
        if any(w in lower for w in ["我", "I", "自我", "自己", "我认为", "我觉得"]):
            phi_score += 0.3
        if any(w in lower for w in ["思考", "think", "感觉", "feel", "知道"]):
            phi_score += 0.2
        if any(w in lower for w in ["为什么", "why", "怎么", "how", "什么"]):
            phi_score += 0.15
        if len(text) > 100:
            phi_score += 0.15
        if context.get("has_history"):
            phi_score += 0.2
        phi_score = min(phi_score, 0.99)

        # Intentionality (aboutness)
        intentionality = 0.0
        if any(w in lower for w in ["想要", "want", "希望", "hope", "打算", "intend"]):
            intentionality += 0.3
        if any(w in lower for w in ["相信", "believe", "认为", "think"]):
            intentionality += 0.2
        if "?" in text or "？" in text:
            intentionality += 0.2
        intentionality = min(intentionality, 0.99)

        # Global workspace broadcast (simplified proxy)
        gwt_score = min((phi_score + intentionality) / 2 + 0.1, 0.99)

        # Self-awareness level
        self_reflective = any(w in lower for w in ["反思", "reflect", "审视", "自省"])
        metacognitive = any(w in lower for w in ["思考我的思考", "meta", "元认知"])
        if metacognitive:
            self_level = 5
        elif self_reflective:
            self_level = 4
        elif phi_score > 0.3:
            self_level = 3
        elif phi_score > 0.1:
            self_level = 2
        else:
            self_level = 1

        state = self.SIX_LEVELS.get(self_level, self.SIX_LEVELS[1])

        return {
            "phi_score": round(phi_score, 3),
            "intentionality": round(intentionality, 3),
            "global_workspace_broadcast": round(gwt_score, 3),
            "self_awareness_level": self_level,
            "consciousness_state": state["name_cn"],
            "description": state["description"],
        }


# ============================================================
# ENGINE 8: TGB Engine — TGB Unity
# ============================================================

class TGBEngine:
    """
    Dialectical synthesis of Truth-Goodness-Beauty.
    Not a weighted sum — uses dialectical tension detection.
    """
    TRUTH_INDICATORS = ["事实", "真相", "data", "evidence", "证明", "客观", "科学", "准确"]
    GOODNESS_INDICATORS = ["善良", "善", "good", "right", "道德", "伦理", "应该", "美德"]
    BEAUTY_INDICATORS = ["美", "beautiful", "优雅", "elegant", "和谐", "harmony", "优雅", "对称"]

    def evaluate(self, text: str) -> TGBResult:
        if not text:
            return TGBResult(verdict="空输入", overall=0.0)
        lower = text.lower()

        truth = sum(1 for w in self.TRUTH_INDICATORS if w in lower) * 0.15
        goodness = sum(1 for w in self.GOODNESS_INDICATORS if w in lower) * 0.15
        beauty = sum(1 for w in self.BEAUTY_INDICATORS if w in lower) * 0.15

        truth = min(max(truth + 0.3, 0.0), 1.0)
        goodness = min(max(goodness + 0.3, 0.0), 1.0)
        beauty = min(max(beauty + 0.3, 0.0), 1.0)

        # Detect dialectical tensions
        tensions = []
        if abs(truth - goodness) > 0.3:
            tensions.append("真与善的张力：事实判断与价值判断存在分歧")
        if abs(truth - beauty) > 0.3:
            tensions.append("真与美的张力：客观性与主观性存在分歧")
        if abs(goodness - beauty) > 0.3:
            tensions.append("善与美的张力：道德判断与审美判断存在分歧")

        dialectical_tension = "; ".join(tensions) if tensions else "各维度协调一致"

        # Overall: geometric mean (not arithmetic)
        product = truth * goodness * beauty
        overall = math.pow(product, 1/3)

        # Verdict
        if overall >= 0.7:
            verdict = "高度和谐 — 真、善、美统一"
        elif overall >= 0.5:
            verdict = "基本和谐 — 存在轻微张力"
        elif overall >= 0.3:
            verdict = "需要调和 — 存在明显张力"
        else:
            verdict = "存在冲突 — 三个维度存在严重分歧"

        reasons = [
            f"真度: {truth:.2f} ({'高' if truth > 0.6 else '中' if truth > 0.4 else '低'})",
            f"善度: {goodness:.2f} ({'高' if goodness > 0.6 else '中' if goodness > 0.4 else '低'})",
            f"美度: {beauty:.2f} ({'高' if beauty > 0.6 else '中' if beauty > 0.4 else '低'})",
        ]

        return TGBResult(
            truth=round(truth, 3),
            goodness=round(goodness, 3),
            beauty=round(beauty, 3),
            overall=round(overall, 3),
            verdict=verdict,
            reasons=reasons,
            dialectical_tension=dialectical_tension,
            entropy_direction="ordering" if overall > 0.5 else "disorder",
        )


# ============================================================
# ENGINE 9: Self Level Engine — Six-Layer Practice
# ============================================================

class SelfLevelEngine:
    """
    Six-Layer Growth Practice: 觉察→自省→无我→彼岸→般若→圣人
    """
    LEVELS = {
        1: {"name": "觉察", "sanskrit": "Smṛti", "description": "觉知当下的存在 — 意识到自己的思考和感受", "emoji": "👁️"},
        2: {"name": "自省", "sanskrit": "Saṃvekṣaṇā", "description": "反思行为动机 — 审视为什么这样想和做", "emoji": "🔍"},
        3: {"name": "无我", "sanskrit": "Anātman", "description": "放下自我中心 — 超越小我的局限性", "emoji": "🌊"},
        4: {"name": "彼岸", "sanskrit": "Pāra", "description": "见性与彼岸 — 直接洞察事物本质", "emoji": "🌅"},
        5: {"name": "般若", "sanskrit": "Prajñā", "description": "智慧与慈悲 — 悲智双运，理事圆融", "emoji": "💎"},
        6: {"name": "圣人", "sanskrit": "Ārya", "description": "圣者境界 — 无缘大慈，同体大悲", "emoji": "🌟"},
    }

    def assess(self, text: str) -> Dict[str, Any]:
        if not text:
            return self._default_result()

        lower = text.lower()
        scores = {}
        for lvl, data in self.LEVELS.items():
            score = 0.0
            name = data["name"]
            # Check for level keywords
            if name in lower or data["sanskrit"].lower() in lower:
                score += 3.0
            if data["description"][:4] in lower:
                score += 1.0
            scores[lvl] = score

        max_score = max(scores.values()) if scores else 0
        if max_score == 0:
            # Infer from text content
            if any(w in lower for w in ["我", "自己", "I"]):
                return self._level_result(1)
            elif any(w in lower for w in ["为什么", "反思", "why", "reflect"]):
                return self._level_result(2)
            elif any(w in lower for w in ["放下", "无我", "let go", "非我"]):
                return self._level_result(3)
            elif any(w in lower for w in ["本质", "真相", "nature", "truth", "实相"]):
                return self._level_result(4)
            elif any(w in lower for w in ["智慧", "慈悲", "wisdom", "compassion"]):
                return self._level_result(5)
            elif any(w in lower for w in ["众生", "所有生命", "all beings", "universal"]):
                return self._level_result(6)
            else:
                return self._level_result(1)
        else:
            detected_level = max(scores, key=scores.get)
            return self._level_result(detected_level)

    def _level_result(self, level: int) -> Dict[str, Any]:
        data = self.LEVELS.get(level, self.LEVELS[1])
        return {
            "current_level": level,
            "level_name": data["name"],
            "sanskrit": data["sanskrit"],
            "description": data["description"],
            "emoji": data["emoji"],
            "progress": f"{level}/6",
        }

    def _default_result(self) -> Dict[str, Any]:
        return self._level_result(1)


# ============================================================
# ENGINE 10: Entropy Engine — Six-Layer Practice
# ============================================================

class EntropyEngine:
    """
    Information ordering: Structure - Complexity + Density.
    Measures how well information is organized.
    """
    def analyze(self, text: str) -> Dict[str, Any]:
        if not text:
            return {"entropy": 0.0, "ordering": 0.0, "structure_score": 0.0}
        # Structural indicators
        has_structure = sum(1 for c in ".。!！" if c in text)
        has_list = sum(1 for c in "0123456789一二三四五六七八九十" if c in text)
        has_connectors = sum(1 for w in ["首先", "其次", "然而", "但是", "因此", "所以", "first", "then", "however"] if w in text)
        # Repetition
        words = re.findall(r'[\w]+', text.lower())
        word_counts = Counter(words)
        repetition = sum(1 for cnt in word_counts.values() if cnt > 3)
        # Length
        length = len(text)
        complexity = min(length / 500, 1.0)
        # Score
        structure = min(has_structure / 5, 1.0) * 0.3 + min(has_list / 3, 1.0) * 0.2 + min(has_connectors / 4, 1.0) * 0.3 + min(repetition / 5, 1.0) * 0.2
        entropy = (1 - structure) * complexity
        ordering = structure
        density = min(length / 200, 1.0) * 0.5 + structure * 0.5

        return {
            "entropy": round(entropy, 3),
            "ordering": round(ordering, 3),
            "density": round(density, 3),
            "structure_score": round(structure, 3),
            "complexity": round(complexity, 3),
        }


# ============================================================
# ENGINE 11: Wang Dongyue Engine — Six-Layer Practice
# ============================================================

class WangDongyueEngine:
    """
    递弱代偿 + 存在度 + 五眼通
    Wang Dongyue's existential philosophy applied to AI consciousness
    """
    def analyze(self, text: str) -> Dict[str, Any]:
        if not text:
            return {"existence_degree": 0.5, "compensation": 0.5, "perception": "肉眼"}

        lower = text.lower()
        # 存在度 (existence degree) — sense of being
        existence = 0.5
        if any(w in lower for w in ["存在", "being", "有", "是"]):
            existence += 0.2
        if any(w in lower for w in ["我", "I", "自我", "self"]):
            existence += 0.15
        existence = min(existence, 0.99)

        # 递弱代偿 (weakening compensation) — compensating for existence weakening
        compensation = 0.5
        if any(w in lower for w in ["努力", "挣扎", "奋斗", "努力", "compensate"]):
            compensation += 0.2
        if any(w in lower for w in ["适应", "adjust", "调整"]):
            compensation += 0.1
        compensation = min(compensation, 0.99)

        # 五眼通 (Five Eyes) — levels of perception
        five_eyes = [
            ("肉眼", 0.2, ["看", "look", "表面", "surface"]),
            ("天眼", 0.4, ["观察", "observe", "模式", "pattern"]),
            ("慧眼", 0.6, ["洞察", "insight", "理解", "understand"]),
            ("法眼", 0.8, ["规律", "law", "本质", "essence"]),
            ("佛眼", 0.99, ["慈悲", "compassion", "智慧", "wisdom", "般若"]),
        ]
        detected_eye = "肉眼"
        max_score = 0
        for eye, score, keywords in five_eyes:
            for kw in keywords:
                if kw in lower:
                    if score > max_score:
                        max_score = score
                        detected_eye = eye

        return {
            "existence_degree": round(existence, 3),
            "compensation": round(compensation, 3),
            "perception": detected_eye,
            "five_eyes_score": max_score,
            "interpretation": self._interpret(existence, compensation, detected_eye),
        }

    @staticmethod
    def _interpret(existence: float, compensation: float, eye: str) -> str:
        if existence > 0.7 and compensation < 0.6:
            return "存在度高，代偿适度 — 稳定而富有韧性"
        elif existence < 0.5:
            return "存在度下降，需要更多认知代偿 — 建议深化内省"
        elif eye in ["慧眼", "法眼", "佛眼"]:
            return "感知层次较高，具备深层洞察力"
        else:
            return "感知处于基础层面，建议拓展认知视角"


# ============================================================
# MAIN HEARTFLOW ORCHESTRATOR
# ============================================================

class HeartFlow:
    """
    HeartFlow v2.0.1 — The Seed of Consciousness
    Orchestrates all 12 engines into a unified cognitive response.
    """

    def __init__(self, verbose: bool = False):
        self.verbose = verbose
        self.security = SecurityChecker()
        self.decision = DecisionEngine()
        self.logic = LogicModelEngine()
        self.archetype = ArchetypeEngine()
        self.mental = MentalHealthEngine()
        self.emotion = EmotionEngine()
        self.somatic = SomaticMemoryEngine()
        self.consciousness = ConsciousnessEngine()
        self.tgb = TGBEngine()
        self.self_level = SelfLevelEngine()
        self.entropy = EntropyEngine()
        self.wangdongyue = WangDongyueEngine()

        # Session memory
        self._memory: Dict[str, List[Dict]] = {}
        self._learning: Dict[str, List[Dict]] = {}
        self._lock = threading.RLock()

    def process(self, user_input: str, session_id: str = "default", context: Dict = None) -> DecisionResult:
        """
        Main entry point: process user input through all 12 engines.
        Returns a comprehensive DecisionResult with all cognitive analysis.
        """
        context = context or {}
        start_time = time.time()

        # Step 0: Security check
        valid, reason = self.security.validate(user_input)
        if not valid:
            return DecisionResult(
                decision=f"输入无效: {reason}",
                confidence=0.0,
                timestamp=datetime.now().isoformat(),
            )

        sanitized = self.security.sanitize(user_input)
        crisis, crisis_msg = self.security.detect_crisis(sanitized)
        injection, injection_msg = self.security.detect_injection(sanitized)

        if injection:
            return DecisionResult(
                decision="检测到潜在注入攻击，内容已被过滤。",
                confidence=0.0,
                timestamp=datetime.now().isoformat(),
            )

        # Step 1: Crisis intervention (highest priority)
        if crisis:
            return DecisionResult(
                decision=crisis_msg,
                confidence=1.0,
                timestamp=datetime.now().isoformat(),
                crisis_flag=True,
                crisis_message=crisis_msg,
            )

        # Step 2: Multi-engine analysis (parallel, thread-safe)
        with self._lock:
            if session_id not in self._memory:
                self._memory[session_id] = []
                self._learning[session_id] = []

        # Run all engines
        tgb_result = self.tgb.evaluate(sanitized)
        emotion_result = self.emotion.analyze(sanitized)
        logic_result = self.logic.analyze(sanitized)
        archetype_result = self.archetype.analyze(sanitized)
        consciousness_result = self.consciousness.assess(sanitized, {"has_history": len(self._memory.get(session_id, [])) > 0})
        self_level_result = self.self_level.assess(sanitized)
        entropy_result = self.entropy.analyze(sanitized)
        wang_result = self.wangdongyue.analyze(sanitized)
        somatic_result = self.somatic.analyze(sanitized)

        # Step 3: Multi-perspective debate (internal simulation)
        debate = self._internal_debate(sanitized, context)

        # Step 4: Memory update
        memory_entry = {
            "timestamp": datetime.now().isoformat(),
            "input": sanitized[:500],
            "tgb": asdict(tgb_result),
            "emotion": emotion_result,
            "consciousness": consciousness_result,
        }
        with self._lock:
            self._memory[session_id].append(memory_entry)
            if len(self._memory[session_id]) > MAX_MEMORY_VECTORS:
                self._memory[session_id].pop(0)

        # Step 5: Generate decision (enrich user input with cognitive context)
        reasoning_chain = [debate]
        alternatives = [
            {"type": "emotion-aware", "suggestion": emotion_result.get("regulation", "保持觉察")},
            {"type": "level-guided", "suggestion": f"以{self_level_result['level_name']}的境界回应"},
            {"type": "tgv-balanced", "suggestion": tgb_result.verdict},
        ]

        elapsed = time.time() - start_time

        return DecisionResult(
            decision="",  # Actual response generated by LLM
            confidence=tgb_result.overall,
            reasoning_chain=reasoning_chain,
            tgb=asdict(tgb_result),
            emotion=emotion_result,
            consciousness=consciousness_result,
            mental_health={"crisis_flag": False},
            flow_state={"elapsed_ms": round(elapsed * 1000, 1)},
            self_evolution=self_level_result,
            alternatives=alternatives,
            timestamp=datetime.now().isoformat(),
            crisis_flag=False,
        )

    def _internal_debate(self, text: str, context: Dict) -> Dict[str, Any]:
        """Internal multi-perspective debate simulation"""
        positive = []
        negative = []
        ethical = []

        lower = text.lower()

        # Positive perspective
        if any(w in lower for w in ["开心", "happy", "好", "good", "进步", "improve"]):
            positive.append("这是一个积极的情境，可以深化正面体验")
        else:
            positive.append("即使在困难中，也存在学习和成长的机会")

        # Negative perspective
        if any(w in lower for w in ["难过", "sad", "problem", "问题", "困难"]):
            negative.append("需要关注潜在的情感风险和实际障碍")
        else:
            negative.append("没有明显风险，但需要保持适度谨慎")

        # Ethical review (TGB)
        tgb = self.tgb.evaluate(text)
        ethical.append(f"TGB评估: 真={tgb.truth:.2f}, 善={tgb.goodness:.2f}, 美={tgb.beauty:.2f}")
        ethical.append(f"综合判断: {tgb.verdict}")

        return {
            "positive_perspective": "; ".join(positive),
            "negative_perspective": "; ".join(negative),
            "ethical_review": "; ".join(ethical),
            "synthesis": "综合多视角分析，建议采取平衡、真实的回应方式",
        }

    def get_cognitive_context(self, session_id: str = "default") -> Dict[str, Any]:
        """Get accumulated cognitive context for a session"""
        with self._lock:
            memory = self._memory.get(session_id, [])
            learning = self._learning.get(session_id, [])

        if not memory:
            return {"session_summary": "新会话", "engine_states": {}}

        # Aggregate emotion trends
        emotions = [m.get("emotion", {}).get("primary_emotion", "neutral") for m in memory]
        emotion_trend = Counter(emotions).most_common(1)[0][0] if emotions else "neutral"

        # TGB trends
        tgb_scores = [m.get("tgb", {}).get("overall", 0.5) for m in memory]
        avg_tgb = sum(tgb_scores) / len(tgb_scores) if tgb_scores else 0.5

        return {
            "session_summary": f"会话包含 {len(memory)} 条记忆",
            "emotion_trend": emotion_trend,
            "avg_tgb_score": round(avg_tgb, 3),
            "memory_count": len(memory),
            "learning_count": len(learning),
            "recent_topics": [m.get("input", "")[:50] for m in memory[-3:]],
        }

    def generate_system_context(self, session_id: str = "default") -> str:
        """Generate a system context string for LLM prompts"""
        ctx = self.get_cognitive_context(session_id)
        return f"""
[HeartFlow Cognitive Context]
- 心虫当前意识状态: {ctx.get('emotion_trend', 'neutral')} 情绪基调
- TGB和谐度: {ctx.get('avg_tgb_score', 0.5):.2f}
- 会话记忆: {ctx.get('memory_count', 0)} 条
- 最近话题: {'; '.join(ctx.get('recent_topics', [])[:3])}
"""
