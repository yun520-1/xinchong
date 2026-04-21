# Conversation Manager — Session and history management
# 心虫 (Xinchong)

import json
import os
import uuid
import time
import threading
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field, asdict
from datetime import datetime
from collections import defaultdict

import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.heartflow import HeartFlow


# ============================================================
# Message Model
# ============================================================

@dataclass
class Message:
    role: str          # user | assistant | system
    content: str
    timestamp: str = ""
    metadata: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        if not self.timestamp:
            self.timestamp = datetime.now().isoformat()

    def to_dict(self) -> Dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, d: Dict) -> "Message":
        return cls(**d)


@dataclass
class Session:
    id: str
    title: str = "新对话"
    created_at: str = ""
    updated_at: str = ""
    messages: List[Dict] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        if not self.created_at:
            self.created_at = datetime.now().isoformat()
        if not self.updated_at:
            self.updated_at = self.created_at

    def add_message(self, role: str, content: str, metadata: Dict = None):
        msg = Message(role=role, content=content, metadata=metadata or {})
        self.messages.append(msg.to_dict())
        self.updated_at = datetime.now().isoformat()

    def to_dict(self) -> Dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, d: Dict) -> "Session":
        return cls(**d)


# ============================================================
# Conversation Manager
# ============================================================

class ConversationManager:
    """
    Manages multiple chat sessions with persistent storage.
    Thread-safe for concurrent access.
    """

    def __init__(self, storage_path: str = "./data/sessions"):
        storage_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            "..", "data", "sessions"
        )
        self.storage_path = os.path.normpath(storage_path)
        self._sessions: Dict[str, Session] = {}
        self._lock = threading.RLock()
        self._heartflow = HeartFlow(verbose=False)
        self._ensure_storage()
        self._load_sessions()

    def _ensure_storage(self):
        os.makedirs(self.storage_path, exist_ok=True)

    def _session_file(self, session_id: str) -> str:
        return os.path.join(self.storage_path, f"{session_id}.json")

    def _load_sessions(self):
        """Load all sessions from disk"""
        try:
            for fname in os.listdir(self.storage_path):
                if fname.endswith(".json"):
                    fpath = os.path.join(self.storage_path, fname)
                    with open(fpath, "r", encoding="utf-8") as f:
                        data = json.load(f)
                    session = Session.from_dict(data)
                    self._sessions[session.id] = session
        except Exception as e:
            print(f"Warning: Failed to load sessions: {e}")

    def _save_session(self, session: Session):
        """Persist session to disk"""
        fpath = self._session_file(session.id)
        with open(fpath, "w", encoding="utf-8") as f:
            json.dump(session.to_dict(), f, ensure_ascii=False, indent=2)

    # ---- Public API ----

    def create_session(self, title: str = "新对话", system_prompt: str = "") -> Session:
        """Create a new session"""
        with self._lock:
            sid = uuid.uuid4().hex[:12]
            session = Session(
                id=sid,
                title=title,
            )
            if system_prompt:
                session.add_message("system", system_prompt)
            self._sessions[sid] = session
            self._save_session(session)
            return session

    def get_session(self, session_id: str) -> Optional[Session]:
        return self._sessions.get(session_id)

    def delete_session(self, session_id: str) -> bool:
        with self._lock:
            if session_id in self._sessions:
                fpath = self._session_file(session_id)
                if os.path.exists(fpath):
                    os.remove(fpath)
                del self._sessions[session_id]
                return True
            return False

    def list_sessions(self) -> List[Dict]:
        """List all sessions (sorted by updated_at desc)"""
        sessions = sorted(
            self._sessions.values(),
            key=lambda s: s.updated_at,
            reverse=True
        )
        return [
            {
                "id": s.id,
                "title": s.title,
                "created_at": s.created_at,
                "updated_at": s.updated_at,
                "message_count": len(s.messages),
            }
            for s in sessions
        ]

    def add_message(self, session_id: str, role: str, content: str, metadata: Dict = None) -> bool:
        """Add a message to a session"""
        with self._lock:
            session = self._sessions.get(session_id)
            if not session:
                return False
            session.add_message(role, content, metadata or {})
            # Auto-title from first user message
            if len(session.messages) == 1 and role == "user":
                session.title = content[:30] + ("..." if len(content) > 30 else "")
            self._save_session(session)
            return True

    def get_messages(self, session_id: str) -> List[Dict]:
        session = self._sessions.get(session_id)
        if not session:
            return []
        return session.messages

    def get_conversation_for_llm(self, session_id: str) -> List[Dict[str, str]]:
        """Get messages in OpenAI format for LLM API"""
        session = self._sessions.get(session_id)
        if not session:
            return []
        return [
            {"role": m["role"], "content": m["content"]}
            for m in session.messages
        ]

    def process_with_heartflow(self, user_input: str, session_id: str) -> Dict[str, Any]:
        """Run HeartFlow cognitive analysis on user input"""
        result = self._heartflow.process(user_input, session_id=session_id)
        return {
            "tgb": result.tgb,
            "emotion": result.emotion,
            "consciousness": result.consciousness,
            "self_evolution": result.self_evolution,
            "reasoning_chain": result.reasoning_chain,
            "alternatives": result.alternatives,
            "crisis_flag": result.crisis_flag,
            "crisis_message": result.crisis_message,
            "confidence": result.confidence,
        }

    def get_cognitive_context(self, session_id: str) -> str:
        """Get HeartFlow cognitive context string"""
        return self._heartflow.generate_system_context(session_id)
