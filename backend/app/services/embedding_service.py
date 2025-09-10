# backend/app/services/embedding_service.py
from sentence_transformers import SentenceTransformer, util
import numpy as np
from typing import List, Tuple, Optional
import torch

class EmbeddingService:
    _instance = None

    def __init__(self, model_name: str):
        self.model_name = model_name
        self.model = SentenceTransformer(model_name)
        self.embeddings = None  # np.ndarray shape (n, dim)
        self.texts = []  # list[str]
        self.meta = []   # list[dict] matching texts

    @classmethod
    def initialize(cls, model_name: str = "sentence-transformers/all-mpnet-base-v2"):
        if cls._instance is None:
            cls._instance = EmbeddingService(model_name)
        return cls._instance

    @classmethod
    def instance(cls):
        if cls._instance is None:
            raise RuntimeError("EmbeddingService not initialized. Call initialize() first.")
        return cls._instance

    def encode_texts(self, texts: List[str], convert_to_numpy: bool = True):
        # use convert_to_tensor for faster cosine on GPU, but CPU fallback works with numpy
        emb = self.model.encode(texts, show_progress_bar=False, convert_to_numpy=convert_to_numpy)
        return emb

    def index(self, texts: List[str], metas: List[dict]):
        self.texts = texts
        self.meta = metas
        self.embeddings = self.encode_texts(texts)

    def query(self, q: str, top_k: int = 3) -> List[Tuple[int, float]]:
        if self.embeddings is None or len(self.embeddings) == 0:
            return []
        q_emb = self.encode_texts([q])[0]
        # cosine similarity
        # Ensure 2D arrays
        emb = self.embeddings
        # compute cosine
        # handle shapes when embeddings are numpy
        scores = util.cos_sim(q_emb, emb)[0].cpu().numpy()
        idxs = np.argsort(-scores)[:top_k]
        return [(int(i), float(scores[i])) for i in idxs]
    def get_embedding_by_index(self, index: int):
        return self.embeddings[index]