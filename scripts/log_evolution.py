#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
scripts/log_evolution.py
📝 生成心智成长日志
"""

import os
import sys
import json
import datetime
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
LOGS_DIR = PROJECT_ROOT / "evolution_logs"


def main():
    os.makedirs(LOGS_DIR, exist_ok=True)

    timestamp = datetime.datetime.now(datetime.timezone.utc)

    # 生成汇总日志
    log = {
        "timestamp": timestamp.isoformat(),
        "type": "evolution_summary",
        "version": "1.0.0",
        "notes": "心智成长汇总 - 由 HeartFlow 进化引擎自动生成",
    }

    # 收集所有论文日志
    paper_logs = sorted(LOGS_DIR.glob("??????_??_??.json"), reverse=True)[:24]

    if paper_logs:
        all_papers = []
        all_engines = set()
        all_suggestions = []

        for log_file in paper_logs:
            try:
                data = json.loads(log_file.read_text(encoding="utf-8"))
                all_papers.extend(data.get("papers", []))
                all_engines.update(data.get("engines_updated", []))
                all_suggestions.extend(data.get("upgrade_suggestions", []))
            except Exception as e:
                print(f"  ⚠️ 读取 {log_file.name} 失败: {e}")

        log["total_papers"] = len(all_papers)
        log["engines_updated"] = sorted(list(all_engines))
        log["unique_suggestions"] = len(set(all_suggestions))
        log["recent_logs"] = [p.name for p in paper_logs[:5]]

    # 保存汇总
    summary_file = LOGS_DIR / "summary.json"
    with open(summary_file, "w", encoding="utf-8") as f:
        json.dump(log, f, ensure_ascii=False, indent=2)

    print(f"✅ 成长日志已更新: {summary_file}")
    print(f"   论文总数: {log.get('total_papers', 0)}")
    print(f"   涉及引擎: {', '.join(log.get('engines_updated', [])) or '无'}")


if __name__ == "__main__":
    main()
