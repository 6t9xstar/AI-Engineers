# 09: High-Throughput Serving with vLLM & PagedAttention

Traditional inference engines suffer severe memory fragmentation in the Key-Value (KV) cache, limiting batch size.

## The PagedAttention Breakthrough
PagedAttention applies OS virtual memory paging concepts to LLM KV caches:
- Divides the KV cache into fixed-size **pages** (e.g. 16 tokens per block).
- Eliminates internal and external memory fragmentation.
- Enables multiple requests to share memory pages (ideal for parallel sampling and beam search).

## Production vLLM Deployment

```bash
python3 -m vllm.entrypoints.openai.api_server \
    --model meta-llama/Llama-3.3-70B-Instruct \
    --tensor-parallel-size 4 \
    --max-model-len 32768 \
    --gpu-memory-utilization 0.92 \
    --enable-chunked-prefill
```
