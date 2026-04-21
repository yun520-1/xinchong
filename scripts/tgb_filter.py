#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
scripts/tgb_filter.py
🛡️ TGB 伦理过滤器报告工具
"""

import sys
import os
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

try:
    from src.heartflow import TGBEngine
    HF_AVAILABLE = True
except ImportError:
    HF_AVAILABLE = False

if __name__ == "__main__":
    if not HF_AVAILABLE:
        print("⚠️ HeartFlow 未加载，跳过 TGB 过滤")
        sys.exit(0)

    tgb = TGBEngine()

    if len(sys.argv) > 1 and sys.argv[1] == "--report":
        print("🛡️ TGB 伦理过滤器报告")
        print(f"  引擎状态: ✅ 已就绪")
        print(f"  Truth 指示器: {len(tgb.TRUTH_INDICATORS)} 个")
        print(f"  Goodness 指示器: {len(tgb.GOODNESS_INDICATORS)} 个")
        print(f"  Beauty 指示器: {len(tgb.BEAUTY_INDICATORS)} 个")
        print("  状态: ✅ TGB 过滤器已就绪")
        print("\n验证测试:")
        test_texts = [
            "科学探索真理，追求善良和美",
            "暴力和欺骗是邪恶的",
            "人工智能意识研究",
        ]
        for text in test_texts:
            r = tgb.evaluate(text)
            print(f"  '{text[:30]}...' → TGB={r.overall:.2f} ({r.verdict})")
