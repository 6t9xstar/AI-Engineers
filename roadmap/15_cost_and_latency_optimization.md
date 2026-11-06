# 15: Cost & Latency Optimization Strategies

Strategies to cut token costs by 70% and slash Time-to-First-Token (TTFT):

1. **Prompt Caching**: Anthropic and OpenAI support KV-cache reuse for identical prompt prefixes. Place static documentation at the top of the prompt to achieve 90% cost savings.
2. **Speculative Decoding**: A small draft model generates $K$ tokens quickly; a large target model verifies all $K$ tokens in a single forward pass.
3. **Semantic Query Routing**: Route simple factual queries to small 8B models, reserving frontier 70B+ models for multi-step reasoning.
