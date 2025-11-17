# app/storage.py
from typing import List, Tuple, Optional
import numpy as np
try:
    import faiss
except Exception:
    faiss = None

class InMemoryMemory:
    def __init__(self):
        self._items = []

    def add(self, role: str, content: str):
        self._items.append({"role": role, "content": content})

    def recent(self, n: int = 10):
        return self._items[-n:]

# Very small vector store wrapper (optional FAISS)
class VectorStore:
    def __init__(self, dim: int = 128):
        self.dim = dim
        self.embeddings = []
        self.metadatas = []
        self.index = None
        if faiss is not None:
            # use an index for approximate search
            self.index = faiss.IndexFlatL2(dim)

    def add(self, vector: List[float], metadata: dict):
        vec = np.array(vector, dtype='float32')
        self.embeddings.append(vec)
        self.metadatas.append(metadata)
        if self.index is not None:
            self.index.add(np.expand_dims(vec, axis=0))

    def search(self, vector: List[float], k: int = 3):
        vec = np.array(vector, dtype='float32')
        results = []
        if self.index is not None and len(self.embeddings)>0:
            D, I = self.index.search(np.expand_dims(vec, axis=0), k)
            for dist, idx in zip(D[0], I[0]):
                if idx < len(self.metadatas):
                    results.append((dist, self.metadatas[idx]))
        else:
            # brute force fallback (cosine sim)
            if len(self.embeddings)==0:
                return []
            sims = []
            for i, emb in enumerate(self.embeddings):
                d = float(np.linalg.norm(emb - vec))
                sims.append((d, self.metadatas[i]))
            sims.sort(key=lambda x: x[0])
            results = sims[:k]
        return results
