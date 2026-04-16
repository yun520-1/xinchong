"""
心虫技能管理系统
"""

import os
import json
import subprocess
from pathlib import Path

# 技能目录
SKILLS_DIR = Path(os.environ.get("XINCHONG_HOME", os.path.expanduser("~/.hermes/xinchong"))) / "skills"


# 内置技能列表
BUILTIN_SKILLS = [
    {"name": "xinchong-core", "description": "核心模块 - 真善美逻辑 + 决策引擎", "tags": ["core", "truth", "goodness", "beauty"]},
    {"name": "xinchong-psychology", "description": "心理模块 - PHQ-9 + GAD-7 心理健康评估", "tags": ["psychology", "mental-health", "phq9", "gad7"]},
    {"name": "xinchong-memory", "description": "记忆模块 - 向量存储 + 长期记忆", "tags": ["memory", "vector", "embedding"]},
    {"name": "xinchong-embodied", "description": "具身认知 - 双系统思维 + 7步推理链", "tags": ["embodied", "cognition", "dual-system"]},
    {"name": "xinchong-dream", "description": "做梦模块 - 深度梦境 + 原型意象", "tags": ["dream", "archetype", "imagery"]},
    {"name": "xinchong-gwt", "description": "全局工作空间 - 意识整合 + 注意广播", "tags": ["gwt", "consciousness", "workspace"]},
    {"name": "xinchong-autonomous", "description": "自主决策 - 三层权限 + 价值判断", "tags": ["autonomous", "decision", "ethics"]},
    {"name": "xinchong-academic", "description": "学术搜索 - 论文检索 + 前沿追踪", "tags": ["academic", "research", "arxiv"]},
    {"name": "xinchong-behavioral", "description": "行为经济 - 16种认知偏误 +助推设计", "tags": ["behavioral", "economics", "biases"]},
]

# OpenClaw 可导入技能
OPENCLAW_SKILLS = [
    {"name": "cn-web-search", "description": "中文网页搜索 - 聚合22+搜索引擎", "tags": ["search", "cn", "web"]},
    {"name": "baidu-search", "description": "百度AI搜索", "tags": ["search", "baidu", "cn"]},
    {"name": "multi-search-engine", "description": "多引擎搜索 - 17种搜索引擎", "tags": ["search", "multi-engine"]},
    {"name": "document-pro", "description": "文档处理 - PDF/DOCX/PPT 解析", "tags": ["document", "pdf", "office"]},
    {"name": "ai-image-generation", "description": "AI图像生成 - FLUX/Gemini/Seedream", "tags": ["image", "generation", "ai"]},
    {"name": "ai-video-generation", "description": "AI视频生成 - Veo/Seedance/Wan", "tags": ["video", "generation", "ai"]},
    {"name": "heartflow", "description": "HeartFlow v7.6 自我进化引擎", "tags": ["heartflow", "self-evolution", "meta-learning"]},
    {"name": "mark-heartflow-skill", "description": "HeartFlow v9 完整版", "tags": ["heartflow", "consciousness", "dreaming"]},
    {"name": "mental-health-analyzer", "description": "心理健康分析 - 睡眠/运动/营养关联", "tags": ["mental-health", "analysis", "wellness"]},
    {"name": "behavioral-product-design", "description": "行为科学产品设计", "tags": ["behavioral", "product", "nudge"]},
    {"name": "marketing-psychology", "description": "营销心理学", "tags": ["marketing", "psychology"]},
    {"name": "cognitive-biases", "description": "认知偏误 - Kahneman/Thaler 原理", "tags": ["cognitive", "biases", "behavioral"]},
    {"name": "ppt-visual", "description": "PPT可视化设计", "tags": ["ppt", "visual", "design"]},
    {"name": "frontend-design", "description": "前端界面设计", "tags": ["frontend", "ui", "design"]},
    {"name": "obsidian", "description": "Obsidian 笔记管理", "tags": ["notes", "obsidian", "markdown"]},
    {"name": "notion", "description": "Notion API 集成", "tags": ["notion", "api", "productivity"]},
    {"name": "google-workspace", "description": "Google 工作空间 - Gmail/Drive/Calendar", "tags": ["google", "workspace", "productivity"]},
    {"name": "linear", "description": "Linear 项目管理", "tags": ["linear", "project", "management"]},
    {"name": "huggingface-hub", "description": "Hugging Face Hub CLI", "tags": ["huggingface", "ml", "models"]},
    {"name": "llama-cpp", "description": "LLM推理 - llama.cpp", "tags": ["llama", "inference", "cpu"]},
    {"name": "gguf", "description": "GGUF量化 - 模型压缩", "tags": ["gguf", "quantization", "compression"]},
    {"name": "whisper", "description": "语音识别 - Whisper", "tags": ["whisper", "speech", "asr"]},
    {"name": "stable-diffusion", "description": "图像生成 - Stable Diffusion", "tags": ["sd", "image", "generation"]},
    {"name": "arxiv", "description": "学术论文搜索 - arXiv", "tags": ["arxiv", "academic", "papers"]},
    {"name": "youtube-content", "description": "YouTube内容获取", "tags": ["youtube", "transcript", "video"]},
    {"name": "gif-search", "description": "GIF搜索 - Tenor", "tags": ["gif", "search", "media"]},
    {"name": "imessage", "description": "iMessage 发送/接收", "tags": ["imessage", "apple", "messaging"]},
    {"name": "apple-notes", "description": "Apple Notes 管理", "tags": ["notes", "apple", "notesapp"]},
    {"name": "apple-reminders", "description": "Apple Reminders 管理", "tags": ["reminders", "apple", "todo"]},
    {"name": "findmy", "description": "FindMy 设备追踪", "tags": ["findmy", "apple", "location"]},
    {"name": "github-pr-workflow", "description": "GitHub PR 工作流", "tags": ["github", "pr", "workflow"]},
    {"name": "github-issues", "description": "GitHub Issues 管理", "tags": ["github", "issues", "tickets"]},
    {"name": "github-code-review", "description": "GitHub 代码审查", "tags": ["github", "review", "code"]},
    {"name": "claude-code", "description": "Claude Code 代理", "tags": ["claude", "agent", "coding"]},
    {"name": "codex", "description": "OpenAI Codex 代理", "tags": ["openai", "codex", "agent"]},
    {"name": "jupyter-live-kernel", "description": "Jupyter 活内核", "tags": ["jupyter", "notebook", "data"]},
    {"name": "modal", "description": "Modal GPU 云服务", "tags": ["modal", "gpu", "cloud"]},
    {"name": "weights-and-biases", "description": "ML实验跟踪 - W&B", "tags": ["ml", "experiment", "tracking"]},
    {"name": "dspy", "description": "DSPy 声明式编程", "tags": ["dspy", "ml", "programming"]},
    {"name": "peft", "description": "PEFT 微调 - LoRA/QLoRA", "tags": ["peft", "finetune", "lora"]},
    {"name": "unsloth", "description": "Unsloth 快速微调", "tags": ["unsloth", "finetune", "fast"]},
]


def list_skills(category: str = None):
    """列出已安装/可用技能"""
    print("\n📦 心虫技能列表\n")
    
    # 内置技能
    print("🧬 内置技能:")
    print(f"{'名称':<30} {'描述':<40}")
    print("-" * 70)
    for s in BUILTIN_SKILLS:
        print(f"{s['name']:<30} {s['description']:<40}")
    print()
    
    # OpenClaw 可导入技能
    print("🔌 OpenClaw 可导入技能:")
    print(f"{'名称':<30} {'描述':<40}")
    print("-" * 70)
    for s in OPENCLAW_SKILLS:
        print(f"{s['name']:<30} {s['description']:<40}")
    print()
    
    # 已安装技能
    if SKILLS_DIR.exists():
        installed = list(SKILLS_DIR.glob("*"))
        installed = [d for d in installed if d.is_dir() and not d.name.startswith(".")]
        if installed:
            print("✅ 已安装技能:")
            for d in installed:
                print(f"  - {d.name}")
            print()


def search_skills(keyword: str):
    """搜索技能"""
    print(f"\n🔍 搜索: {keyword}\n")
    
    keyword = keyword.lower()
    results = []
    seen = set()
    
    # 搜索内置技能
    for s in BUILTIN_SKILLS:
        if keyword in s["name"].lower() or keyword in s["description"].lower():
            key = s["name"]
            if key not in seen:
                seen.add(key)
                results.append(("内置", s))
    
    # 搜索 OpenClaw 技能
    for s in OPENCLAW_SKILLS:
        if keyword in s["name"].lower() or keyword in s["description"].lower():
            key = s["name"]
            if key not in seen:
                seen.add(key)
                results.append(("OpenClaw", s))
        # 搜索标签
        elif any(keyword in tag.lower() for tag in s.get("tags", [])):
            key = s["name"]
            if key not in seen:
                seen.add(key)
                results.append(("OpenClaw", s))
    
    if results:
        print(f"{'类型':<10} {'名称':<30} {'描述':<40}")
        print("-" * 80)
        for typ, s in results:
            print(f"{typ:<10} {s['name']:<30} {s['description']:<40}")
    else:
        print("未找到匹配技能")
    print()


def install_skill(skill_name: str):
    """安装技能"""
    print(f"\n📥 安装技能: {skill_name}\n")
    
    # 检查是否是内置技能
    for s in BUILTIN_SKILLS:
        if s["name"] == skill_name:
            print(f"⚠️ {skill_name} 是内置技能，无需安装")
            return
    
    # 检查是否是 OpenClaw 技能
    openclaw_skill = None
    for s in OPENCLAW_SKILLS:
        if s["name"] == skill_name:
            openclaw_skill = s
            break
    
    if not openclaw_skill:
        print(f"❌ 未找到技能: {skill_name}")
        print("使用 xinchong skills 查看可用技能")
        return
    
    # 创建技能目录
    SKILLS_DIR.mkdir(parents=True, exist_ok=True)
    
    # OpenClaw 技能位于 ~/.hermes/skills/
    src = Path.home() / ".hermes" / "skills" / skill_name
    dst = SKILLS_DIR / skill_name
    
    if src.exists():
        # 复制技能目录
        import shutil
        if dst.exists():
            print(f"⚠️ {skill_name} 已存在，跳过")
        else:
            shutil.copytree(src, dst)
            print(f"✅ {skill_name} 安装成功！")
            print(f"   位置: {dst}")
    else:
        # 尝试使用 opencode plugin 安装
        print(f"从 OpenClaw 导入 {skill_name}...")
        result = subprocess.run(
            ["opencode", "plugin", skill_name, "-g"],
            capture_output=True,
            text=True,
            timeout=120
        )
        
        if result.returncode == 0:
            # 再次检查
            src = Path.home() / ".hermes" / "skills" / skill_name
            if src.exists():
                import shutil
                dst = SKILLS_DIR / skill_name
                if dst.exists():
                    print(f"⚠️ {skill_name} 已存在，跳过")
                else:
                    shutil.copytree(src, dst)
                    print(f"✅ {skill_name} 安装成功！")
            else:
                print(f"✅ {skill_name} 已安装到全局")
        else:
            print(f"❌ 安装失败")
            if result.stderr:
                print(f"   {result.stderr[:200]}")
            print("可能是技能名称不正确，请检查后重试")


def remove_skill(skill_name: str):
    """移除技能"""
    print(f"\n🗑️ 移除技能: {skill_name}\n")
    
    skill_dir = SKILLS_DIR / skill_name
    if skill_dir.exists():
        import shutil
        shutil.rmtree(skill_dir)
        print(f"✅ {skill_name} 已移除")
    else:
        print(f"❌ {skill_name} 未安装")


def init_skills():
    """初始化技能目录"""
    SKILLS_DIR.mkdir(parents=True, exist_ok=True)
    print(f"技能目录: {SKILLS_DIR}")
