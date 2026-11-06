# Efficient Memory Management for Large Language Model Serving with PagedAttention (Kwon et al., 2023)
- **Core Breakthrough**: Inspired by virtual memory OS paging, partitions KV cache into non-contiguous physical blocks.
- **Impact**: Powered vLLM, cutting memory waste from 70% to under 4% and boosting throughput 4x.
