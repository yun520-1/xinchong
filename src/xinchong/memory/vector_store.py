"""
向量记忆系统 - 语义搜索 + 存在性记忆
"""

import json
import os
import hashlib
from datetime import datetime
from pathlib import Path
from typing import Optional, List, Dict, Tuple
import numpy as np


class VectorMemory:
    """向量记忆系统 - 支持语义搜索"""
    
    def __init__(self, storage_dir: str = "~/.xinchong/memory"):
        self.storage_dir = Path(os.path.expanduser(storage_dir))
        self.storage_dir.mkdir(parents=True, exist_ok=True)
        
        # 文件路径
        self.vectors_file = self.storage_dir / "vectors.json"
        self.dreams_file = self.storage_dir / "dreams.json"
        self.existence_file = self.storage_dir / "existence.json"
        
        self._init_files()
    
    def _init_files(self):
        """初始化文件"""
        if not self.vectors_file.exists():
            self._save_json(self.vectors_file, {
                "memories": [], "version": "2.0", "dimension": 1536
            })
        if not self.dreams_file.exists():
            self._save_json(self.dreams_file, {"dreams": [], "version": "1.0"})
        if not self.existence_file.exists():
            self._save_json(self.existence_file, {"entities": [], "version": "1.0"})
    
    def _save_json(self, file_path: Path, data: dict):
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    def _load_json(self, file_path: Path) -> dict:
        if file_path.exists():
            with open(file_path, encoding="utf-8") as f:
                return json.load(f)
        return {}
    
    def _get_embedding(self, text: str) -> List[float]:
        """获取文本 embedding（使用本地简单 hash 模拟）"""
        # 实际应该调用 embedding API
        # 这里用简单的 hash 作为占位符
        hash_val = hashlib.sha256(text.encode()).digest()
        # 转换为 0-1 之间的浮点数
        return [b / 255.0 for b in hash_val[:64]]  # 简化版
    
    def _cosine_similarity(self, a: List[float], b: List[float]) -> float:
        """计算余弦相似度"""
        if not a or not b:
            return 0.0
        a = np.array(a)
        b = np.array(b)
        return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b) + 1e-8))
    
    # ===== 记忆操作 =====
    def add_memory(self, content: str, category: str = "general",
                   importance: int = 5, metadata: dict = None) -> dict:
        """添加记忆（带向量）"""
        data = self._load_json(self.vectors_file)
        
        # 生成向量
        embedding = self._get_embedding(content)
        
        memory = {
            "id": len(data.get("memories", [])) + 1,
            "content": content,
            "category": category,
            "importance": importance,  # 1-10 重要性
            "embedding": embedding,
            "created_at": datetime.now().isoformat(),
            "last_accessed": datetime.now().isoformat(),
            "access_count": 0,
            "metadata": metadata or {},
            "tags": self._extract_tags(content)
        }
        
        data.setdefault("memories", []).append(memory)
        self._save_json(self.vectors_file, data)
        
        return {"success": True, "memory_id": memory["id"]}
    
    def _extract_tags(self, content: str) -> List[str]:
        """提取标签"""
        # 简单提取：空格分隔的词
        words = content.lower().split()
        # 过滤停用词
        stop_words = {"的", "是", "在", "了", "和", "与", "或", "但", "而", "着", "被", "把", "给", "到", "从", "为", "以", "等"}
        return [w for w in words if len(w) > 1 and w not in stop_words][:10]
    
    def recall(self, query: str, limit: int = 5, min_similarity: float = 0.3) -> List[dict]:
        """语义检索记忆"""
        data = self._load_json(self.vectors_file)
        
        query_embedding = self._get_embedding(query)
        memories = data.get("memories", [])
        
        # 计算相似度
        results = []
        for mem in memories:
            sim = self._cosine_similarity(query_embedding, mem.get("embedding", []))
            if sim >= min_similarity:
                results.append({
                    **mem,
                    "similarity": sim
                })
        
        # 按相似度排序
        results.sort(key=lambda x: x["similarity"], reverse=True)
        
        # 更新访问次数
        for r in results[:limit]:
            for mem in memories:
                if mem["id"] == r["id"]:
                    mem["last_accessed"] = datetime.now().isoformat()
                    mem["access_count"] = mem.get("access_count", 0) + 1
        self._save_json(self.vectors_file, data)
        
        return results[:limit]
    
    def search_by_tags(self, tags: List[str], limit: int = 10) -> List[dict]:
        """按标签搜索"""
        data = self._load_json(self.vectors_file)
        memories = data.get("memories", [])
        
        results = []
        for mem in memories:
            mem_tags = set(mem.get("tags", []))
            query_tags = set(tags)
            # 计算标签重叠
            overlap = len(mem_tags & query_tags)
            if overlap > 0:
                results.append({**mem, "tag_match": overlap})
        
        results.sort(key=lambda x: x["tag_match"], reverse=True)
        return results[:limit]
    
    # ===== 做梦操作 =====
    def add_dream(self, content: str, dream_type: str = "normal",
                   emotions: List[str] = None, context: dict = None) -> dict:
        """记录梦境"""
        data = self._load_json(self.dreams_file)
        
        dream = {
            "id": len(data.get("dreams", [])) + 1,
            "content": content,
            "type": dream_type,  # normal, nightmare, lucid, prophetic
            "emotions": emotions or [],
            "created_at": datetime.now().isoformat(),
            "context": context or {}
        }
        
        data.setdefault("dreams", []).append(dream)
        self._save_json(self.dreams_file, data)
        
        return {"success": True, "dream_id": dream["id"]}
    
    def get_recent_dreams(self, limit: int = 10) -> List[dict]:
        """获取最近梦境"""
        data = self._load_json(self.dreams_file)
        dreams = data.get("dreams", [])
        return dreams[-limit:] if dreams else []
    
    def dream_interpret(self, dream_id: int = None) -> dict:
        """梦境解读（简化版）"""
        data = self._load_json(self.dreams_file)
        dreams = data.get("dreams", [])
        
        if dream_id:
            dream = next((d for d in dreams if d["id"] == dream_id), None)
        else:
            dream = dreams[-1] if dreams else None
        
        if not dream:
            return {"error": "No dream found"}
        
        # 简单的符号解读
        symbols = {
            "falling": "失去控制感 / 焦虑",
            "flying": "渴望自由 / 突破限制",
            "water": "情感 / 潜意识",
            "fire": "激情 / 愤怒",
            "death": "结束 / 新生",
            "chase": "逃避 / 压力",
            "lost": "迷茫 / 自我怀疑"
        }
        
        content_lower = dream["content"].lower()
        found_symbols = [k for k in symbols if k in content_lower]
        
        return {
            "dream": dream,
            "interpretations": [symbols.get(s, "未知符号") for s in found_symbols],
            "emotions": dream.get("emotions", []),
            "type": dream.get("type", "normal")
        }
    
    # ===== 存在性记忆 =====
    def add_entity(self, entity_type: str, name: str, 
                   attributes: dict = None) -> dict:
        """添加实体（用户、概念、关系）"""
        data = self._load_json(self.existence_file)
        
        entity = {
            "id": len(data.get("entities", [])) + 1,
            "type": entity_type,  # user, concept, relationship
            "name": name,
            "attributes": attributes or {},
            "created_at": datetime.now().isoformat(),
            "last_interaction": datetime.now().isoformat()
        }
        
        data.setdefault("entities", []).append(entity)
        self._save_json(self.existence_file, data)
        
        return {"success": True, "entity_id": entity["id"]}
    
    def get_entity(self, name: str = None, entity_type: str = None) -> List[dict]:
        """查询实体"""
        data = self._load_json(self.existence_file)
        entities = data.get("entities", [])
        
        results = entities
        if name:
            results = [e for e in results if name in e.get("name", "")]
        if entity_type:
            results = [e for e in results if e.get("type") == entity_type]
        
        return results
    
    def update_interaction(self, name: str):
        """更新交互时间"""
        data = self._load_json(self.existence_file)
        entities = data.get("entities", [])
        
        for e in entities:
            if e.get("name") == name:
                e["last_interaction"] = datetime.now().isoformat()
                e["interaction_count"] = e.get("interaction_count", 0) + 1
        
        self._save_json(self.existence_file, data)
    
    # ===== 统计 =====
    def get_stats(self) -> dict:
        """获取记忆统计"""
        memory_data = self._load_json(self.vectors_file)
        dream_data = self._load_json(self.dreams_file)
        entity_data = self._load_json(self.existence_file)
        
        return {
            "total_memories": len(memory_data.get("memories", [])),
            "total_dreams": len(dream_data.get("dreams", [])),
            "total_entities": len(entity_data.get("entities", [])),
            "categories": self._count_by_category(memory_data.get("memories", [])),
            "importance_distribution": self._distribution(memory_data.get("memories", []), "importance")
        }
    
    def _count_by_category(self, memories: List[dict]) -> dict:
        categories = {}
        for m in memories:
            cat = m.get("category", "unknown")
            categories[cat] = categories.get(cat, 0) + 1
        return categories
    
    def _distribution(self, items: List[dict], key: str) -> dict:
        dist = {}
        for item in items:
            val = item.get(key, 0)
            dist[val] = dist.get(val, 0) + 1
        return dist


# 全局实例
vector_memory = VectorMemory()