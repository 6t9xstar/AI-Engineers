"""
Hybrid Search (Dense Vector + BM25 Sparse Keyword) with Reciprocal Rank Fusion (RRF)
Author: 6t9xstar (AI-Engineers)
License: MIT

Demonstrates production hybrid retrieval combining dense semantic similarity
with exact keyword matching, fused via Reciprocal Rank Fusion.
"""

import math
import re
from collections import Counter
from typing import List, Dict, Any, Tuple

class SimpleBM25:
    """Minimal, self-contained BM25 Okapi lexical retriever."""
    def __init__(self, corpus: List[str], k1: float = 1.5, b: float = 0.75):
        self.k1 = k1
        self.b = b
        self.corpus = corpus
        self.doc_len = [len(self._tokenize(doc)) for doc in corpus]
        self.avg_doc_len = sum(self.doc_len) / len(self.doc_len) if self.doc_len else 0
        self.doc_freqs: List[Counter] = [Counter(self._tokenize(doc)) for doc in corpus]
        self.idf: Dict[str, float] = self._compute_idf()

    def _tokenize(self, text: str) -> List[str]:
        return re.findall(r"\w+", text.lower())

    def _compute_idf(self) -> Dict[str, float]:
        df = Counter()
        for doc in self.doc_freqs:
            df.update(doc.keys())
        N = len(self.corpus)
        return {word: math.log((N - freq + 0.5) / (freq + 0.5) + 1.0) for word, freq in df.items()}

    def score(self, query: str) -> List[Tuple[int, float]]:
        q_tokens = self._tokenize(query)
        scores = []
        for idx, doc_freq in enumerate(self.doc_freqs):
            score = 0.0
            doc_l = self.doc_len[idx]
            for token in q_tokens:
                if token in doc_freq:
                    freq = doc_freq[token]
                    idf = self.idf.get(token, 0.0)
                    denom = freq + self.k1 * (1 - self.b + self.b * (doc_l / self.avg_doc_len))
                    score += idf * (freq * (self.k1 + 1)) / denom
            scores.append((idx, score))
        scores.sort(key=lambda x: x[1], reverse=True)
        return scores

class MockDenseEmbedder:
    """Simulates a dense vector embedder using token co-occurrence hash vectors."""
    def embed(self, text: str, dims: int = 128) -> List[float]:
        vec = [0.0] * dims
        tokens = re.findall(r"\w+", text.lower())
        for t in tokens:
            idx = hash(t) % dims
            vec[idx] += 1.0
        # Normalize L2
        norm = math.sqrt(sum(x * x for x in vec)) or 1.0
        return [x / norm for x in vec]

def cosine_similarity(v1: List[float], v2: List[float]) -> float:
    return sum(a * b for a, b in zip(v1, v2))

def reciprocal_rank_fusion(
    bm25_ranked: List[Tuple[int, float]],
    dense_ranked: List[Tuple[int, float]],
    k: int = 60
) -> List[Tuple[int, float]]:
    """Combines dense and sparse rankings using Reciprocal Rank Fusion (RRF)."""
    rrf_scores: Dict[int, float] = {}

    for rank, (doc_id, _) in enumerate(bm25_ranked):
        rrf_scores[doc_id] = rrf_scores.get(doc_id, 0.0) + (1.0 / (k + (rank + 1)))

    for rank, (doc_id, _) in enumerate(dense_ranked):
        rrf_scores[doc_id] = rrf_scores.get(doc_id, 0.0) + (1.0 / (k + (rank + 1)))

    ranked = sorted(rrf_scores.items(), key=lambda x: x[1], reverse=True)
    return ranked

# ==========================================
# Self-Test Verification
# ==========================================
if __name__ == "__main__":
    docs = [
        "ShadowCLI provides zero-trust kernel sandboxing for AI coding agents using Linux Landlock LSM.",
        "BM25 is a ranking function used by search engines to estimate the relevance of documents to a given search query.",
        "Model Context Protocol (MCP) connects LLMs to tools using JSON-RPC STDIO transport.",
        "Cross-encoders score query and document pairs simultaneously to provide superior reranking precision.",
        "PostgreSQL pgvector allows dense semantic vector similarity search using HNSW indexes."
    ]

    query = "How does ShadowCLI sandbox agent tool calls?"
    print(f"Query: {query}\n")

    # 1. Lexical BM25 Search
    bm25 = SimpleBM25(docs)
    bm25_res = bm25.score(query)

    # 2. Dense Vector Search
    embedder = MockDenseEmbedder()
    q_vec = embedder.embed(query)
    dense_res = []
    for idx, d in enumerate(docs):
        sim = cosine_similarity(q_vec, embedder.embed(d))
        dense_res.append((idx, sim))
    dense_res.sort(key=lambda x: x[1], reverse=True)

    # 3. Fuse via RRF
    hybrid_res = reciprocal_rank_fusion(bm25_res, dense_res)

    print("--- Top Hybrid RRF Results ---")
    for doc_id, rrf_score in hybrid_res[:3]:
        print(f"[RRF Score: {rrf_score:.5f}] Doc #{doc_id}: {docs[doc_id]}")
