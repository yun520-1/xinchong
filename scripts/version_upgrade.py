#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
scripts/version_upgrade.py
🔢 心虫版本升级脚本
每次调用版本号 +0.0.1，并更新所有相关文件。
"""

import os
import sys
import re
import datetime
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
HEARTFLOW_FILE = PROJECT_ROOT / "src" / "heartflow.py"
CONFIG_FILE = PROJECT_ROOT / "config.yaml"
README_FILE = PROJECT_ROOT / "README.md"
REQUIREMENTS_FILE = PROJECT_ROOT / "requirements.txt"

# 版本文件
VERSION_FILE = PROJECT_ROOT / "VERSION.txt"


def read_version() -> str:
    """读取当前版本"""
    if VERSION_FILE.exists():
        return VERSION_FILE.read_text().strip()
    # 从 heartflow.py 读取
    if HEARTFLOW_FILE.exists():
        content = HEARTFLOW_FILE.read_text(encoding="utf-8")
        m = re.search(r'__version__\s*=\s*["\']([^"\']+)["\']', content)
        if m:
            return m.group(1)
    return "1.0.0"


def parse_version(v: str) -> tuple:
    """解析版本号为 (major, minor, patch) — 使用整数避免浮点精度问题"""
    # 移除后缀如 -xinchong
    v = v.split("-")[0]
    parts = v.split(".")
    while len(parts) < 3:
        parts.append("0")
    # 用整数表示 patch*10 来存储小数版本（如 patch=1 表示 0.1）
    major = int(parts[0])
    minor = int(parts[1])
    patch_tenths = int(round(float(f"0.{parts[2]}" if len(parts) > 2 and parts[2] else "0") * 10))
    return major, minor, patch_tenths


def format_version(major: int, minor: int, patch_tenths: int) -> str:
    """格式化版本号"""
    return f"{major}.{minor}.{patch_tenths}"


def bump_version(current: str, increment: str = "patch") -> str:
    """升级版本号（每次 +0.1）"""
    major, minor, patch_tenths = parse_version(current)
    if increment == "minor":
        minor += 1
        patch_tenths = 0
    elif increment == "major":
        major += 1
        minor = 0
        patch_tenths = 0
    else:  # patch: +0.1
        patch_tenths += 1
        if patch_tenths >= 10:
            patch_tenths = 0
            minor += 1
        if minor >= 10:
            minor = 0
            major += 1
    return format_version(major, minor, patch_tenths)


def upgrade_version(new_version: str):
    """升级所有文件中的版本号"""
    timestamp = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    changes = []

    # 1. VERSION.txt
    VERSION_FILE.write_text(new_version, encoding="utf-8")
    changes.append("VERSION.txt")

    # 2. src/heartflow.py
    if HEARTFLOW_FILE.exists():
        content = HEARTFLOW_FILE.read_text(encoding="utf-8")
        new_content = re.sub(
            r'__version__\s*=\s*["\'][^"\']+["\']',
            f'__version__ = "{new_version}"',
            content
        )
        # Also update the version comment
        new_content = re.sub(
            r'HeartFlow v[\d.]+',
            f"HeartFlow v{new_version}",
            new_content
        )
        HEARTFLOW_FILE.write_text(new_content, encoding="utf-8")
        changes.append("src/heartflow.py")

    # 3. config.yaml (app.version)
    if CONFIG_FILE.exists():
        content = CONFIG_FILE.read_text(encoding="utf-8")
        new_content = re.sub(
            r'version:\s*["\'][^"\']+["\']',
            f'version: "{new_version}"',
            content
        )
        CONFIG_FILE.write_text(new_content, encoding="utf-8")
        changes.append("config.yaml")

    # 4. README.md badge
    if README_FILE.exists():
        content = README_FILE.read_text(encoding="utf-8")
        new_content = re.sub(
            r'v[\d.]+',
            new_version,
            content,
            count=1
        )
        README_FILE.write_text(new_content, encoding="utf-8")
        changes.append("README.md")

    # 5. 生成 CHANGELOG entry
    changelog_file = PROJECT_ROOT / "CHANGELOG.md"
    changelog_entry = f"""## [{new_version}] - {timestamp[:10]}

### 🤖 自动升级
- 心智升级：版本 +0.0.1
- 触发时间: {timestamp}
- 变更文件: {', '.join(changes)}

"""
    if changelog_file.exists():
        old_content = changelog_file.read_text(encoding="utf-8")
        changelog_file.write_text(changelog_entry + old_content, encoding="utf-8")
    else:
        changelog_file.write_text(f"# Changelog\n\n{changelog_entry}", encoding="utf-8")

    return changes


def main():
    if len(sys.argv) > 1 and sys.argv[1] == "--get":
        print(read_version())
        return

    current = read_version()
    new = bump_version(current)

    print(f"🔢 版本升级: {current} → {new}")

    changes = upgrade_version(new)
    print(f"✅ 已更新: {', '.join(changes)}")
    print(f"📝 CHANGELOG.md 已追加")
    print(f"🆕 新版本: {new}")


if __name__ == "__main__":
    main()
