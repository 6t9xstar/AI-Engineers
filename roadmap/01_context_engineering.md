# 01: Context Engineering & LLM Memory Management

Context is the working memory of the modern Large Language Model. How you design, structure, and budget tokens directly dictates whether an AI agent succeeds or hallucinates.

---

## 1. The Anatomy of Modern Context Windows

While modern frontier models boast context windows ranging from **128,000 to 2,000,000 tokens**, context capacity does not equal context utilization.

### The "Lost in the Middle" Phenomenon
Research by Liu et al. proves that LLMs retrieve information with highest fidelity from the **very beginning (primacy effect)** and the **very end (recency effect)** of the context window. Information placed in the middle 60% suffers retrieval degradation of up to 40%.

```
Retrieval Accuracy
 100% |  ***                                                     ***
      |  *  *                                                   *  *
  80% |  *   *                                                 *   *
      |  *    *                                               *    *
  60% |  *     *                                             *     *
      |         *                                           *
  40% |          *******************************************
      +-------------------------------------------------------------+
      0% (System Prompt)      50% (Middle Context)     100% (User Question)
```

### Optimal Context Layout
1. **Top (0–10%)**: Core System Directives, Behavioral Constraints, and Tool Schemas.
2. **Upper-Middle (10–50%)**: Persistent Knowledge Base, Reference Data, and Documentation.
3. **Lower-Middle (50–85%)**: Historical Conversation Turns & Execution Traces.
4. **Bottom (85–100%)**: Retrieved RAG Context, Current User Query, and Strict Output Instructions.

---

## 2. Dynamic Token Budgeting Strategies

In production agentic loops, context grows monotonically with each turn. Without active budgeting, systems hit token limits, degrade in reasoning quality, and balloon API costs.

### Windowed Slotted Memory Architecture

```python
class ContextBudgetManager:
    """Allocates rigid token budgets across cognitive context slots."""
    def __init__(self, max_tokens: int = 128_000):
        self.max_tokens = max_tokens
        # Budget allocations
        self.system_budget = int(max_tokens * 0.15)      # 15%
        self.rag_budget = int(max_tokens * 0.35)         # 35%
        self.history_budget = int(max_tokens * 0.35)     # 35%
        self.scratchpad_budget = int(max_tokens * 0.15)  # 15% (generation headroom)
```

### Semantic Compression
When historical turns exceed the budget, apply **hierarchical summarization**:
1. Keep the last `K` turns (e.g. 4 turns) in full raw fidelity.
2. Compress turns `0` to `N-K` into structured state summaries:
   - *Decisions Made*: Bulleted list of confirmed technical choices.
   - *Active Tasks*: Current uncompleted objectives.
   - *Variable State*: In-flight variables and file paths modified.

---

## 3. Semantic Caching Architecture

Repetitive agent queries and static context fragments can be cached at the semantic layer to eliminate latency and inference expense.

### Cache Lookup Pipeline
1. Compute dense vector embedding of the user intent: $E(q) = \text{EmbeddingModel}(q)$.
2. Query vector store for similar previously answered prompts.
3. If cosine similarity $\text{sim}(E(q), E(q_k)) \ge 0.94$, return cached answer with verification metadata.
4. Otherwise, route to LLM and persist response.

---

## Next Steps
Proceed to [02: Production RAG & Advanced Retrieval](02_production_rag.md).
