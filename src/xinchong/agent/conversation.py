"""
对话历史管理
"""

import json
import os
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional


class ConversationManager:
    """对话历史管理"""
    
    def __init__(self, storage_dir: str = "~/.xinchong"):
        self.storage_dir = Path(os.path.expanduser(storage_dir))
        self.conversations_dir = self.storage_dir / "conversations"
        self.conversations_dir.mkdir(parents=True, exist_ok=True)
        
        self.current_session_id = None
        self.messages: List[Dict] = []
    
    def start_session(self, session_id: str = None) -> str:
        """开始新会话"""
        if session_id is None:
            session_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        self.current_session_id = session_id
        self.messages = []
        
        # 加载历史会话
        session_file = self.conversations_dir / f"{session_id}.json"
        if session_file.exists():
            with open(session_file, encoding="utf-8") as f:
                data = json.load(f)
                self.messages = data.get("messages", [])
        
        return session_id
    
    def add_message(self, role: str, content: str):
        """添加消息"""
        self.messages.append({
            "role": role,  # "user" or "assistant"
            "content": content,
            "timestamp": datetime.now().isoformat()
        })
    
    def get_messages(self, limit: int = None) -> List[Dict]:
        """获取消息列表"""
        if limit:
            return self.messages[-limit:]
        return self.messages
    
    def save_session(self):
        """保存当前会话"""
        if not self.current_session_id:
            return
        
        session_file = self.conversations_dir / f"{self.current_session_id}.json"
        
        data = {
            "session_id": self.current_session_id,
            "created_at": self.messages[0]["timestamp"] if self.messages else datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat(),
            "message_count": len(self.messages),
            "messages": self.messages
        }
        
        with open(session_file, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    def list_sessions(self, limit: int = 10) -> List[Dict]:
        """列出最近会话"""
        sessions = []
        for f in sorted(self.conversations_dir.glob("*.json"), key=lambda x: x.stat().st_mtime, reverse=True):
            with open(f, encoding="utf-8") as fp:
                data = json.load(fp)
                sessions.append({
                    "session_id": data["session_id"],
                    "created_at": data["created_at"],
                    "message_count": data["message_count"]
                })
                if len(sessions) >= limit:
                    break
        return sessions
    
    def load_session(self, session_id: str):
        """加载指定会话"""
        self.start_session(session_id)


# 全局实例
conversation = ConversationManager()