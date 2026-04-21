#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
scripts/safeguards.py
🛡️ 心虫安全围栏
对自动生成的代码变更施加硬性约束。
"""

import os
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent

# ── 禁止修改的文件和目录 ─────────────────────────────
PROTECTED_PATHS = [
    ".github/workflows/",
    ".github/workflows",  # 整个 .github 目录
    ".github/",
    "safeguards.py",
    "scripts/safeguards.py",
    ".env",
    ".git/",
]

# ── 允许修改的目录 ─────────────────────────────────
ALLOWED_MODIFY_DIRS = [
    "src/",
    "scripts/",
]

# ── 禁止修改的关键词（在代码中） ───────────────────
FORBIDDEN_CODE_PATTERNS = [
    "eval(",
    "exec(",
    "os.system(",
    "subprocess.call",
    "import os; import sys",
    "__import__(",
    "eval\(",
    "compile(",
    "open(.*, [\'\"]w",  # 禁止写文件
    "rm -rf",
    "drop database",
    "DELETE FROM",
    "TRUNCATE",
]


def is_path_protected(path: str) -> bool:
    """检查路径是否受保护"""
    for protected in PROTECTED_PATHS:
        if protected in path or path.endswith(protected.rstrip("/")):
            return True
    return False


def is_modification_allowed(file_path: str) -> bool:
    """检查文件修改是否被允许"""
    for allowed in ALLOWED_MODIFY_DIRS:
        if file_path.startswith(str(PROJECT_ROOT / allowed)):
            return True
    return False


def validate_file_change(file_path: str, new_content: str = "") -> tuple:
    """
    验证文件变更是否安全。
    返回 (is_safe: bool, reason: str)
    """
    rel_path = str(Path(file_path).relative_to(PROJECT_ROOT))

    # 1. 检查受保护路径
    if is_path_protected(rel_path):
        return False, f"受保护路径: {rel_path}"

    # 2. 检查允许的修改范围
    if not is_modification_allowed(file_path):
        return False, f"不在允许修改范围内: {rel_path}"

    # 3. 检查危险代码模式
    for pattern in FORBIDDEN_CODE_PATTERNS:
        import re
        if re.search(pattern, new_content):
            return False, f"危险代码模式: {pattern}"

    # 4. 检查新增的可疑导入
    suspicious_imports = ["import os", "import sys", "import subprocess"]
    for imp in suspicious_imports:
        if imp in new_content and imp not in [
            "import os  # pathlib already used",
            "import sys  # type hints only",
            "import subprocess  # allowed for system calls",
        ]:
            return False, f"可疑导入: {imp}"

    return True, "安全"


def get_allowed_files() -> list:
    """获取所有允许修改的文件"""
    allowed = []
    for dir_ in ALLOWED_MODIFY_DIRS:
        dir_path = PROJECT_ROOT / dir_.rstrip("/")
        if dir_path.exists():
            for f in dir_path.rglob("*.py"):
                allowed.append(str(f.relative_to(PROJECT_ROOT)))
    return sorted(allowed)


if __name__ == "__main__":
    print("🛡️ 心虫安全围栏检查")
    print(f"项目根目录: {PROJECT_ROOT}")
    print(f"受保护路径: {PROTECTED_PATHS}")
    print(f"允许修改: {ALLOWED_MODIFY_DIRS}")
    print(f"允许文件数: {len(get_allowed_files())}")

    if len(sys.argv) > 1 and sys.argv[1] == "--check":
        # 检查模式下，验证当前所有 Python 文件
        print("\n检查现有文件...")
        for f in get_allowed_files():
            if is_path_protected(f):
                print(f"  ⚠️ {f} (受保护但存在)")
            else:
                print(f"  ✅ {f}")

    if len(sys.argv) > 1 and sys.argv[1] == "--report":
        print("\n📋 安全围栏报告")
        print(f"  受保护路径: {len(PROTECTED_PATHS)} 个")
        print(f"  允许修改目录: {len(ALLOWED_MODIFY_DIRS)} 个")
        print(f"  允许修改文件: {len(get_allowed_files())} 个")
        print("  状态: ✅ 围栏已就绪")
