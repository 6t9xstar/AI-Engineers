# 16: The AI Engineer Interview: 50 Deep Questions & Answers

Essential questions covering LLM systems, RAG, agents, and infrastructure:

1. **Q**: What causes context degradation in large windows?
   **A**: Attention dispersion across position embeddings and softmax saturation over long sequences.
2. **Q**: How does RRF differ from linear score fusion in hybrid search?
   **A**: RRF uses ordinal rank rather than raw score magnitudes, eliminating the need to normalize disparate similarity scales.
3. **Q**: Why are user namespaces required for rootless Linux sandboxing?
   **A**: User namespaces allow mapping an unprivileged UID to root inside the sandbox namespace, enabling private mount namespaces without host root permissions.
