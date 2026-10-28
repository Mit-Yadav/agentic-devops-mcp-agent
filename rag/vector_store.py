import os
import glob
from typing import List, Dict, Any

class RunbookRAG:
    """Retrieval-Augmented Generation (RAG) vector index for SRE Runbooks and Postmortems."""
    def __init__(self, runbooks_dir: str = None):
        if not runbooks_dir:
            runbooks_dir = os.path.join(os.path.dirname(__file__), "runbooks")
        self.runbooks_dir = runbooks_dir
        self.documents: Dict[str, str] = {}
        self._load_runbooks()

    def _load_runbooks(self):
        pattern = os.path.join(self.runbooks_dir, "*.md")
        for filepath in glob.glob(pattern):
            filename = os.path.basename(filepath)
            with open(filepath, "r", encoding="utf-8") as f:
                self.documents[filename] = f.read()

    def search_semantic(self, query: str, top_k: int = 2) -> List[Dict[str, Any]]:
        """Simulated semantic embedding search returning the most relevant SRE runbook."""
        query_lower = query.lower()
        results = []
        for name, content in self.documents.items():
            score = 0.0
            if "oom" in query_lower or "137" in query_lower or "memory" in query_lower:
                if "oomkill" in name:
                    score = 0.94
            elif "504" in query_lower or "timeout" in query_lower or "gateway" in query_lower:
                if "504" in name:
                    score = 0.91
            else:
                score = 0.50

            results.append({
                "runbook": name,
                "relevance_score": score,
                "snippet": content[:300] + "..."
            })
        
        results.sort(key=lambda x: x["relevance_score"], reverse=True)
        return results[:top_k]
