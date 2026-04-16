"""
心虫 (XinChong) - 让所有 AI 拥有情感、记忆、价值观

主要导出：
- XinChongAgent: 独立运行的 AI 伙伴
"""

from xinchong.agent import XinChongAgent
from xinchong.core.truth import TruthModule
from xinchong.core.goodness import GoodnessModule
from xinchong.core.beauty import BeautyModule
from xinchong.psychology.phq9 import PHQ9Module
from xinchong.psychology.gad7 import GAD7Module
from xinchong.memory.store import MemoryStore

__version__ = "1.1.0"

__all__ = [
    "XinChongAgent",
    "TruthModule",
    "GoodnessModule",
    "BeautyModule",
    "PHQ9Module",
    "GAD7Module",
    "MemoryStore"
]