# Vector Database Architecture Matrix (2026)

| Engine | Language | Index Types | Filtering | Deployment |
|---|---|---|---|---|
| Qdrant | Rust | HNSW | In-payload graph traversal | Self-hosted / Cloud |
| Pinecone | Proprietary | Proprietary | Metadata indexing | Managed Serverless |
| Milvus | Go/C++ | HNSW, IVF-PQ, DiskANN | Scalar partition | Distributed Kubernetes |
| pgvector | C (Postgres) | HNSW, IVFFlat | SQL WHERE clauses | PostgreSQL native |
| Chroma | Python/Rust | HNSW | In-memory / DuckDB | Local / Embedded |
