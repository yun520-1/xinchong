#!/usr/bin/env python3
"""
心虫 (Xinchong) — Web Entry Point
Run: python run_web.py
Opens: http://localhost:8765
"""

import os
import sys

# Load .env if exists
env_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env")
if os.path.exists(env_path):
    with open(env_path, "r") as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                key, val = line.split("=", 1)
                os.environ.setdefault(key.strip(), val.strip())

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.web.app import app

if __name__ == "__main__":
    cfg = app.config.get("XINCHONG_CFG", {})
    host = cfg.get("app", {}).get("host", "0.0.0.0")
    port = cfg.get("app", {}).get("port", 8765)
    debug = cfg.get("app", {}).get("debug", False)

    print(f"""
╔═══════════════════════════════════════════╗
║    🐛 心虫 (Xinchong) Web Interface      ║
║         http://{host}:{port}            ║
╚═══════════════════════════════════════════╝
""")
    app.run(host=host, port=port, debug=debug, threaded=True)
