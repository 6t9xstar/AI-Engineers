# 02: Production RAG & Advanced Retrieval Architectures

Naive vector search (`embed_text -> vector_db -> top_k`) works for simple demos but fails in production. Real-world documents contain specialized terminology, part numbers, code identifiers, and dense tables that cosine similarity alone cannot reliably resolve.

---

## 1. Why Naive Vector Search Fails

1. **Semantic Drift**: A vector embedding collapses 1,000 words into 1,536 floating-point numbers. Precise keyword nuances (e.g. `CVE-2024-38063` vs `CVE-2024-38064`) get smoothed out.
2. **Chunk Fragmentation**: Fixed-size chunking (e.g., 500 characters) cuts sentences in half, splitting context across artificial boundaries.
3. **Keyword Blindness**: Rare identifiers, API endpoints, variable names, and error codes often have poor dense embeddings compared to common natural language.

---

## 2. The Gold Standard: Hybrid Search with Reciprocal Rank Fusion (RRF)

Production retrieval pairs **Dense Semantic Search** (Bi-Encoder embeddings like `text-embedding-3-large` or `bge-large-en-v1.5`) with **Sparse Keyword Search** (BM25 or SPLADE).

```
User Query
   |
   +-------------------+-------------------+
   |                                       |
   v                                       v
Dense Vector Search               Sparse BM25 Search
(Cosine Similarity)               (Exact Lexical Match)
   |                                       |
   +-------------------+-------------------+
                       |
                       v
            Reciprocal Rank Fusion (RRF)
                       |
                       v
         Cross-Encoder Reranker (Top-K)
                       |
                       v
            Filtered Context to LLM
```

### Reciprocal Rank Fusion (RRF) Formula
RRF fuses rankings without requiring score normalization:

$$RRF(d) = \sum_{m \in M} \frac{1}{k + r_m(d)}$$

Where:
- $M$ is the set of retrieval models (Dense + BM25).
- $r_m(d)$ is the rank of document $d$ in system $m$.
- $k$ is a constant smoothing parameter (typically $k = 60$).

---

## 3. Two-Stage Retrieval & Cross-Encoder Reranking

Bi-encoders generate embeddings for queries and documents independently. They are fast ($O(1)$ vector index lookups), but cannot model cross-attention between specific query tokens and document tokens.

A **Cross-Encoder Reranker** passes the query and document candidate together through a transformer layer:

$$\text{Score} = \text{CrossEncoder}([\text{Query}, \text{Document}])$$

### Production Pipeline
1. **Stage 1 (Retrieval)**: Fetch top 50 candidates using Hybrid Search (Dense + BM25).
2. **Stage 2 (Reranking)**: Score all 50 candidates through a cross-encoder model (e.g. `bge-reranker-large` or Cohere Rerank v3).
3. **Stage 3 (Truncation)**: Feed only the top 5 highest-confidence chunks into the LLM context.

---

## 4. Chunking Strategies Compared

| Strategy | Ideal For | Drawback |
|---|---|---|
| **Recursive Character** | General Prose, Markdown | Ignores document semantics |
| **Semantic Boundary** | Academic Papers, Long-form Essays | Higher compute cost to compute split embeddings |
| **AST / Syntax-Aware** | Codebases (Python, Rust, TS) | Requires language-specific parsers |
| **Hierarchical / Parent-Child** | Large enterprise manuals | Requires tracking parent/child metadata references |

---

## Next Steps
Proceed to [03: Autonomous Agent Patterns](03_agent_patterns.md).
