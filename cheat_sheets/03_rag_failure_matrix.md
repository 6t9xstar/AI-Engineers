# The 7 Failure Points of RAG & Production Fixes

1. **Missing Content**: Document not ingested -> Expand indexing crawler.
2. **Missed Top Chunks**: Dense embedding smoothed keyword -> Switch to Hybrid Search (Dense + BM25).
3. **Not in Context**: Chunk dropped by Top-K -> Increase Top-K to 50 and use a Cross-Encoder Reranker.
4. **Not Extracted**: Model lost info in the middle -> Re-order context or use context compression.
5. **Wrong Format**: LLM outputted prose instead of JSON -> Enforce schema with Instructor/Pydantic.
6. **Incorrect Specificity**: Chunk was too granular or broad -> Use Parent-Child / Hierarchical chunking.
7. **Incomplete**: Query required multi-hop synthesis -> Implement GraphRAG community summaries.
