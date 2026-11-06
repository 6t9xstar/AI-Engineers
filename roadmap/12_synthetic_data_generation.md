# 12: Synthetic Data Generation & Distillation Pipelines

High-quality domain-specific data is the biggest bottleneck in enterprise AI development. Synthetic data bridges the gap.

## Generation Methodologies

### 1. Evol-Instruct
Takes baseline seed instructions and applies evolutionary operators:
- **In-Depth Evolution**: Add constraints, deepen reasoning, increase complexity.
- **In-Breadth Evolution**: Generate mutated topics and lateral applications.

### 2. Self-Consistency Rejection Sampling
1. Generate $N$ candidate responses with high temperature ($T = 0.8$).
2. Verify answers with deterministic test suites or execution compilers.
3. Filter out failing traces, keeping only verified reasoning paths for fine-tuning.
