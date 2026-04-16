"""
记忆永存模块
"""

import json
import os
from datetime import datetime
from pathlib import Path
from typing import Optional, List, Dict


class MemoryStore:
    """记忆存储"""
    
    def __init__(self, storage_dir: str = "~/.xinchong/memory"):
        self.storage_dir = Path(os.path.expanduser(storage_dir))
        self.storage_dir.mkdir(parents=True, exist_ok=True)
        
        # 记忆文件
        self.memories_file = self.storage_dir / "memories.json"
        self.sessions_file = self.storage_dir / "sessions.json"
        
        # 初始化
        self._init_files()
    
    def _init_files(self):
        """初始化记忆文件"""
        if not self.memories_file.exists():
            self._save_json(self.memories_file, {"memories": [], "version": "1.0"})
        
        if not self.sessions_file.exists():
            self._save_json(self.sessions_file, {"sessions": [], "version": "1.0"})
    
    def _save_json(self, file_path: Path, data: dict):
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    def _load_json(self, file_path: Path) -> dict:
        if file_path.exists():
            with open(file_path, encoding="utf-8") as f:
                return json.load(f)
        return {}
    
    # ===== 记忆操作 =====
    def add_memory(self, content: str, category: str = "general", 
                   metadata: dict = None) -> dict:
        """添加记忆"""
        memories = self._load_json(self.memories_file)
        
        memory = {
            "id": len(memories.get("memories", [])) + 1,
            "content": content,
            "category": category,
            "created_at": datetime.now().isoformat(),
            "metadata": metadata or {}
        }
        
        memories.setdefault("memories", []).append(memory)
        self._save_json(self.memories_file, memories)
        
        return {"success": True, "memory_id": memory["id"]}
    
    def recall(self, query: str, limit: int = 5) -> List[dict]:
        """记忆检索（简单关键词匹配）"""
        memories = self._load_json(self.memories_file)
        
        results = []
        for mem in memories.get("memories", []):
            if query.lower() in mem["content"].lower():
                results.append(mem)
                if len(results) >= limit:
                    break
        
        return results
    
    def get_all(self, category: str = None) -> List[dict]:
        """获取所有记忆"""
        memories = self._load_json(self.memories_file)
        mems = memories.get("memories", [])
        
        if category:
            return [m for m in mems if m.get("category") == category]
        return mems
    
    # ===== 会话操作 =====
    def save_session(self, session_id: str, messages: List[dict]):
        """保存会话"""
        sessions = self._load_json(self.sessions_file)
        
        sessions.setdefault("sessions", []).append({
            "session_id": session_id,
            "messages": messages,
            "created_at": datetime.now().isoformat()
        })
        
        self._save_json(self.sessions_file, sessions)
    
    def get_recent_sessions(self, limit: int = 10) -> List[dict]:
        """获取最近会话"""
        sessions = self._load_json(self.sessions_file)
        all_sessions = sessions.get("sessions", [])
        return all_sessions[-limit:] if all_sessions else []


# 全局实例
memory = MemoryStore()