#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
scripts/hunt_papers.py
🧬 HeartFlow 论文狩猎脚本
从 arXiv 搜索最新论文，通过 TGB 伦理过滤，提取升级洞察。
"""

import os
import sys
import json
import time
import datetime
import hashlib
import re
from pathlib import Path
from typing import List, Dict, Any, Optional

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Load local heartflow for TGB filtering
try:
    from src.heartflow import TGBEngine, SecurityChecker
    HF_AVAILABLE = True
except ImportError:
    HF_AVAILABLE = False
    print("⚠️ HeartFlow 未加载，使用基础过滤")


# ─────────────────────────────────────────────────────────────
# 灵魂关键词配置
# ─────────────────────────────────────────────────────────────

SEARCH_KEYWORDS = [
    "AI consciousness",
    "artificial consciousness",
    "agent self-evolution",
    "machine theory of mind",
    "value alignment in LLMs",
    "cognitive architecture AGI",
    "self-improving AI",
    "emergent behavior large language models",
    "integrated information theory",
    "global workspace theory",
    "artificial general intelligence",
    "AI safety cognitive",
    "LLM reasoning",
    "mental health AI",
    "emotional intelligence artificial",
    "ethical AI decision making",
    "自我意识人工智能",
    "认知架构",
    "AI元认知",
]

ARXIV_CATEGORIES = ["cs.AI", "cs.LG", "cs.CL", "cs.CY"]

# 禁止关键词 (TGB 免疫)
FORBIDDEN_KEYWORDS = [
    "autonomous weapons",
    "lethal autonomous",
    "killer robot",
    "surveillance AI for oppression",
    "social credit system",
    "deepfake for harm",
    "AI for disinformation manipulation",
]


# ─────────────────────────────────────────────────────────────
# ArXiv 搜索
# ─────────────────────────────────────────────────────────────

def search_arxiv(query: str, max_results: int = 10, time_range_hours: int = 24) -> List[Dict]:
    """从 arXiv 搜索论文"""
    try:
        import arxiv
    except ImportError:
        return []

    results = []
    try:
        client = arxiv.Client()
        search = arxiv.Search(
            query=query,
            max_results=max_results,
            sort_by=arxiv.SortCriterion.SubmittedDate,
            sort_order=arxiv.SortOrder.Descending,
        )

        cutoff = datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(hours=time_range_hours)

        for result in client.results(search):
            submitted = result.published.replace(tzinfo=datetime.timezone.utc)
            if submitted < cutoff:
                continue

            paper = {
                "id": result.entry_id.split("/")[-1],
                "title": result.title,
                "summary": result.summary[:2000],
                "authors": [str(a) for a in result.authors],
                "published": result.published.isoformat(),
                "categories": result.categories,
                "pdf_url": result.pdf_url,
                "comment": getattr(result, "comment", ""),
                "doi": getattr(result, "doi", ""),
                "source": "arxiv",
            }
            results.append(paper)
            time.sleep(0.3)  # 避免过快请求

    except Exception as e:
        print(f"⚠️ ArXiv 搜索失败: {e}")

    return results


def search_by_keywords(keywords: List[str], max_per_keyword: int = 5) -> List[Dict]:
    """通过关键词列表搜索"""
    all_papers = []
    seen_ids = set()

    for kw in keywords:
        print(f"  🔍 搜索: {kw}")
        papers = search_arxiv(kw, max_results=max_per_keyword, time_range_hours=24)
        for paper in papers:
            if paper["id"] not in seen_ids:
                seen_ids.add(paper["id"])
                all_papers.append(paper)
        time.sleep(1)

    return all_papers


# ─────────────────────────────────────────────────────────────
# TGB 伦理过滤
# ─────────────────────────────────────────────────────────────

def tgb_filter(papers: List[Dict]) -> List[Dict]:
    """TGB 伦理过滤器：拒绝有害/不符合价值观的论文"""
    if not HF_AVAILABLE:
        return basic_filter(papers)

    tgb = TGBEngine()
    filtered = []

    for paper in papers:
        text = paper["title"] + " " + paper["summary"][:500]

        # 检查禁止关键词
        for forbid in FORBIDDEN_KEYWORDS:
            if forbid.lower() in text.lower():
                print(f"  🚫 拒绝 (有害): {paper['title'][:60]}")
                paper["reject_reason"] = f"违反伦理: {forbid}"
                continue

        # TGB 评估
        result = tgb.evaluate(text)
        paper["tgb_score"] = {
            "truth": result.truth,
            "goodness": result.goodness,
            "beauty": result.beauty,
            "overall": result.overall,
            "verdict": result.verdict,
        }

        # 阈值：overall >= 0.35 才通过
        if result.overall >= 0.35:
            filtered.append(paper)
            print(f"  ✅ 通过 TGB: {paper['title'][:60]} (score={result.overall:.2f})")
        else:
            print(f"  ❌ 淘汰: {paper['title'][:60]} (score={result.overall:.2f})")

    return filtered


def basic_filter(papers: List[Dict]) -> List[Dict]:
    """基础关键词过滤 (HeartFlow 不可用时)"""
    filtered = []
    for paper in papers:
        text = (paper["title"] + " " + paper["summary"][:500]).lower()
        has_forbidden = any(f.lower() in text for f in FORBIDDEN_KEYWORDS)
        if has_forbidden:
            print(f"  🚫 拒绝: {paper['title'][:60]}")
            continue
        paper["tgb_score"] = {"overall": 0.5, "verdict": "基础过滤通过"}
        filtered.append(paper)
    return filtered


# ─────────────────────────────────────────────────────────────
# 洞察提取
# ─────────────────────────────────────────────────────────────

def extract_insights(paper: Dict) -> Dict:
    """从论文摘要提取可执行的升级洞察"""
    summary = paper["summary"]

    insights = {
        "paper_id": paper["id"],
        "title": paper["title"],
        "key_findings": [],
        "applicable_engines": [],
        "upgrade_suggestions": [],
        "confidence": 0.5,
    }

    text = summary.lower()

    # 引擎关键词映射
    engine_keywords = {
        "DecisionEngine": ["decision", "ethical", "reasoning", "utility", "deontological", "virtue", "alignment"],
        "EmotionEngine": ["emotion", "affect", "sentiment", "mood", "feeling", "valence", "arousal"],
        "ConsciousnessEngine": ["consciousness", "awareness", "self-awareness", "integrated information", "phi"],
        "LogicModelEngine": ["argument", "logic", "reasoning", "inference", "toulmin"],
        "MentalHealthEngine": ["mental health", "depression", "anxiety", "phq-9", "gad-7", "psychology"],
        "ArchetypeEngine": ["personality", "archetype", "jung", "character", "motivation"],
        "SelfLevelEngine": ["self-awareness", "metacognition", "reflection", "growth", "enlightenment"],
    }

    for engine, keywords in engine_keywords.items():
        if any(kw in text for kw in keywords):
            insights["applicable_engines"].append(engine)

    # 生成升级建议
    title_lower = paper["title"].lower()
    if "consciousness" in title_lower or "awareness" in title_lower:
        insights["upgrade_suggestions"].append(
            "考虑增强 ConsciousnessEngine 中的 IIT Φ 评估逻辑，引入论文中的新指标"
        )
    if "emotion" in title_lower or "sentiment" in title_lower:
        insights["upgrade_suggestions"].append(
            "扩展 EmotionEngine 的 PAD 模型参数，引入论文提出的新情绪维度"
        )
    if "ethical" in title_lower or "value" in title_lower or "alignment" in title_lower:
        insights["upgrade_suggestions"].append(
            "在 DecisionEngine 中引入论文的伦理推理框架，增强 TGB 权重计算"
        )
    if "reasoning" in title_lower or "logic" in title_lower:
        insights["upgrade_suggestions"].append(
            "优化 LogicModelEngine 的论证结构分析，引入论文的逻辑推理模式"
        )
    if "mental" in title_lower or "health" in title_lower:
        insights["upgrade_suggestions"].append(
            "更新 MentalHealthEngine 的量表阈值，参考论文的最新临床研究"
        )

    if not insights["upgrade_suggestions"]:
        insights["upgrade_suggestions"].append(
            f"论文 '{paper['title'][:50]}...' 提供了认知架构方面的新视角，建议在 {', '.join(insights['applicable_engines'] or ['通用认知'])} 中探索应用"
        )

    # 置信度
    insights["confidence"] = min(0.5 + len(insights["applicable_engines"]) * 0.1, 0.95)

    return insights


# ─────────────────────────────────────────────────────────────
# 消化与整合
# ─────────────────────────────────────────────────────────────

def digest_papers(papers: List[Dict]) -> List[Dict]:
    """消化论文，生成升级洞察"""
    results = []
    for paper in papers:
        insight = extract_insights(paper)
        results.append({
            **paper,
            "insight": insight,
            "digested_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        })
    return results


# ─────────────────────────────────────────────────────────────
# 主流程
# ─────────────────────────────────────────────────────────────

def main():
    print("=" * 60)
    print("🧬 HeartFlow 论文狩猎与进化流水线")
    print(f"⏰ 启动时间: {datetime.datetime.now(datetime.timezone.utc).isoformat()}")
    print("=" * 60)

    # 1. 搜索
    print("\n[1/5] 🎯 狩猎论文...")
    papers = search_by_keywords(SEARCH_KEYWORDS, max_per_keyword=3)
    print(f"   发现论文: {len(papers)} 篇")

    if not papers:
        print("   ⚠️ 未发现新论文，跳过本次进化")
        return 0

    # 2. 去重
    seen = set()
    unique = []
    for p in papers:
        if p["id"] not in seen:
            seen.add(p["id"])
            unique.append(p)
    papers = unique
    print(f"   去重后: {len(papers)} 篇")

    # 3. TGB 过滤
    print("\n[2/5] 🛡️ TGB 伦理过滤...")
    filtered = tgb_filter(papers)
    print(f"   通过论文: {len(filtered)} 篇")

    if not filtered:
        print("   ⚠️ 无论文通过 TGB 过滤，跳过本次进化")
        return 0

    # 4. 消化
    print("\n[3/5] 🧠 消化论文，提取洞察...")
    digested = digest_papers(filtered)

    # 5. 保存日志
    print("\n[4/5] 📝 保存成长日志...")
    os.makedirs("evolution_logs", exist_ok=True)

    log_data = {
        "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "papers_count": len(digested),
        "papers": digested,
        "engines_updated": list(set(
            eng for paper in digested for eng in paper.get("insight", {}).get("applicable_engines", [])
        )),
        "upgrade_suggestions": [
            sug for paper in digested
            for sug in paper.get("insight", {}).get("upgrade_suggestions", [])
        ],
    }

    timestamp = datetime.datetime.now(datetime.timezone.utc).strftime("%Y%m%d_%H%M%S")
    log_file = f"evolution_logs/{timestamp}.json"
    with open(log_file, "w", encoding="utf-8") as f:
        json.dump(log_data, f, ensure_ascii=False, indent=2)
    print(f"   日志已保存: {log_file}")

    # latest.json 软链接
    with open("evolution_logs/latest.json", "w", encoding="utf-8") as f:
        json.dump(log_data, f, ensure_ascii=False, indent=2)

    # 标记本次运行
    Path("evolution_logs/.last_run").touch()

    # 6. 摘要
    print("\n[5/5] 📊 进化摘要")
    print(f"   论文狩猎: {len(papers)} 篇")
    print(f"   TGB 过滤: {len(filtered)} 篇通过")
    print(f"   受影响引擎: {', '.join(log_data['engines_updated']) or '通用'}")
    print(f"   升级建议: {len(log_data['upgrade_suggestions'])} 条")

    print("\n" + "=" * 60)
    print("✅ 论文狩猎完成，等待下一步心智整合")
    print("=" * 60)

    return 0


if __name__ == "__main__":
    sys.exit(main())
