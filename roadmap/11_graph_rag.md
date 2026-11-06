# 11: GraphRAG & Knowledge Graph Augmented Retrieval

Standard vector RAG answers "needle-in-a-haystack" queries well, but fails at global questions requiring multi-hop synthesis across entire corpora.

## GraphRAG Architecture
1. **Entity & Relationship Extraction**: LLM extracts entities (Nodes) and relationships (Edges) from document chunks.
2. **Community Detection (Leiden Algorithm)**: Partitions the graph into hierarchical clusters of related concepts.
3. **Community Summarization**: Generates pre-computed summaries for each cluster at macro and micro levels.
4. **Global Querying**: Synthesizes answers by querying cluster summaries rather than raw vector chunks.
