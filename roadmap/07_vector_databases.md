# 07: Vector Databases & Indexing Strategies

Vector databases store high-dimensional embeddings and perform Approximate Nearest Neighbor (ANN) search.

## Core Indexing Algorithms

### 1. Hierarchical Navigable Small World (HNSW)
HNSW builds a multi-layered graph where upper layers have longer links (fast skip-list style traversal) and bottom layers have dense local links.
- **Pros**: Exceptional query throughput and recall (>98%).
- **Cons**: High RAM overhead for graph storage.

### 2. Inverted File Index with Product Quantization (IVF-PQ)
Clusters vectors into Voronoi cells, then compresses vectors by dividing them into sub-vectors and quantizing to cluster centroids.
- **Pros**: 90% memory reduction, scalable to billions of vectors.
- **Cons**: Lower recall; requires training phase on representative dataset.

## Vector Engine Comparison (2026)

| Engine | Storage | Best For | Standout Feature |
|---|---|---|---|
| **Qdrant** | Rust / In-memory & Mmap | Production RAG | Native payload filtering during HNSW traversal |
| **Pinecone** | Cloud Managed | Serverless Scale | Zero-ops serverless architecture |
| **Milvus** | Distributed Go/C++ | 100M+ Vectors | Decoupled compute and storage |
| **pgvector** | PostgreSQL extension | Existing Relational DBs | Joins relational SQL tables with vector embeddings |
