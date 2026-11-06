# The AI Engineer's Handbook & Production Toolkit (2026)

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python: 3.10+](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![TypeScript: 5.x](https://img.shields.io/badge/TypeScript-5.x-blue.svg)](https://www.typescriptlang.org/)
[![MCP Standard: 2024--11--05](https://img.shields.io/badge/MCP-Compatible-green.svg)](https://modelcontextprotocol.io/)
[![Zero-Trust Security](https://img.shields.io/badge/Security-Zero--Trust%20Sandboxed-purple.svg)](https://github.com/6t9xstar/shadowcli)

An authoritative, production-grade guide, architectural reference, and working code cookbook for modern **AI Engineers**. Covers everything from Context Engineering and Advanced RAG to Autonomous Multi-Agent Swarms, Model Context Protocol (MCP), and Zero-Trust Execution Sandboxes.

---

## 📑 Table of Contents

- [The AI Engineer Periodic Table](#-the-ai-engineer-periodic-table)
- [Architecture Roadmaps](#-architecture-roadmaps)
  - [1. Context Engineering & LLM Foundations](roadmap/01_context_engineering.md)
  - [2. Production RAG & Retrieval Pipelines](roadmap/02_production_rag.md)
  - [3. Autonomous Agent Patterns & Workflows](roadmap/03_agent_patterns.md)
  - [4. The Model Context Protocol (MCP) Standard](roadmap/04_mcp_standard.md)
  - [5. Evaluations, Guardrails & LLM-as-a-Judge](roadmap/05_guardrails_evals.md)
  - [6. Zero-Trust Agent Sandboxing & Security](roadmap/06_agent_sandboxing.md)
- [Cookbook & Runnable Code](#-cookbook--runnable-code)
  - [Hybrid Search (Dense + BM25 + RRF)](cookbook/rag/hybrid_search.py)
  - [ReAct Agent Loop from Scratch](cookbook/agents/react_agent.py)
  - [Structured Outputs with Pydantic](cookbook/structured_outputs/instructor_pydantic.py)
  - [Production MCP Server with Tool Dispatch](cookbook/mcp/mcp_server.py)
  - [LLM-as-a-Judge Evaluation Pipeline](cookbook/evals/llm_as_judge.py)
- [Production System Prompts](templates/system_prompts.md)
- [Contributing & License](#-contributing)

---

## 🧱 The AI Engineer Periodic Table

```
+---------------------------------------------------------------------------------------+
|                                THE AI ENGINEER STACK                                  |
+---------------------------------------------------------------------------------------+
|  ORCHESTRATION   | LangGraph | AutoGen | CrewAI | LlamaIndex | PydanticAI | Swarms     |
|  RAG / RETRIEVAL | Hybrid Dense+BM25 | Reciprocal Rank Fusion | Cohere/BGE Rerankers  |
|  TOOL PROTOCOL   | Model Context Protocol (MCP) | JSON-RPC STDIO | SSE Streaming      |
|  STRUCTURED OUT  | Pydantic v2 | Instructor | Zod | JSON Schema Strict Enforcement    |
|  EVALS & JUDGES  | Ragas | DeepEval | TruLens | G-Eval | Brier Calibration Score      |
|  LOCAL SERVING   | vLLM | Ollama | llama.cpp | TensorRT-LLM | ExLlamaV2               |
|  ZERO-TRUST SAND | Landlock LSM | Unshare Namespaces | ShadowCLI CoW OverlayFS       |
+---------------------------------------------------------------------------------------+
```

---

## 🗺 Architecture Roadmaps

### 1. [Context Engineering & Memory Management](roadmap/01_context_engineering.md)
- Mitigating the *"Lost in the Middle"* syndrome in 128k–1M context windows.
- Dynamic Token Budgeting & Context Compression strategies.
- Semantic Caching (GPTCache, Redis semantic indexing) to cut latency by 85%.

### 2. [Production RAG & Advanced Retrieval](roadmap/02_production_rag.md)
- Why naive vector search fails in production (dense semantic drift).
- Hybrid Search architecture: Combining dense vector similarity (cosine) with BM25 sparse keyword scoring via **Reciprocal Rank Fusion (RRF)**.
- Cross-Encoder reranking (BGE-Reranker-Large, Cohere v3).
- Hierarchical, Semantic, and Markdown chunking strategies.

### 3. [Autonomous Agent Patterns](roadmap/03_agent_patterns.md)
- **ReAct (Reason + Act)**: The core inner thought, action, and observation loop.
- **Plan-and-Solve**: Decoupling high-level task decomposition from tool execution.
- **Reflexion & Self-Correction**: Dynamic backoff and error recovery patterns.
- **Hierarchical Multi-Agent Supervisors**: Managing specialized worker nodes.

### 4. [Model Context Protocol (MCP) Standard](roadmap/04_mcp_standard.md)
- Anthropic's open MCP architecture: Connecting frontier models to real-world tools.
- Designing stateful vs stateless MCP tools over JSON-RPC STDIO.
- Tool discovery, dynamic schema negotiation, and streaming tool results.

### 5. [Evaluations, Guardrails & LLM-as-a-Judge](roadmap/05_guardrails_evals.md)
- Evaluating the RAG Triad: Context Relevance, Groundedness (Faithfulness), and Answer Relevance.
- Guardrails against Prompt Injection, Indirect Jailbreaks, and Data Exfiltration.
- Deterministic Schema Validation with automatic error feedback loops.

### 6. [Zero-Trust Agent Sandboxing & Security](roadmap/06_agent_sandboxing.md)
- **The Core Problem**: Why giving an AI agent unrestricted terminal access (`bash`) inevitably leads to catastrophic host destruction (`rm -rf`, credential theft, socket hijacking).
- **The Solution**: Containerless Linux kernel sandboxing using unprivileged user namespaces (`CLONE_NEWUSER`), transient `tmpfs` mounts, Landlock LSM, and ephemeral Copy-on-Write overlays via [ShadowCLI](https://github.com/6t9xstar/shadowcli).

---

## 🍳 Cookbook & Code Examples

Every recipe in `cookbook/` is standalone, tested, and ready to drop into production:

### 1. Hybrid Search with Reciprocal Rank Fusion
```python
# cookbook/rag/hybrid_search.py
# Combines Dense Vector + BM25 with Reciprocal Rank Fusion (RRF)
from cookbook.rag.hybrid_search import HybridRetriever

retriever = HybridRetriever(docs=[...])
results = retriever.search("What is Landlock LSM?", top_k=5)
```

### 2. ReAct Agent Loop from Scratch
```python
# cookbook/agents/react_agent.py
# Pure Python ReAct loop without heavy framework dependencies
from cookbook.agents.react_agent import ReActAgent, Tool

agent = ReActAgent(tools=[search_tool, calculator_tool])
response = agent.run("Find the latest release of ShadowCLI and count its stars")
```

### 3. Model Context Protocol (MCP) Server
```python
# cookbook/mcp/mcp_server.py
# Production STDIO JSON-RPC 2.0 server for Claude Code and Cursor
python cookbook/mcp/mcp_server.py
```

---

## 🛡 Security Philosophy

Autonomous agents are executing code in the real world. This repository adheres to the **Principle of Least Privilege**:
- All tool execution must be staged in ephemeral Copy-on-Write overlays.
- Outbound network egress must be disabled by default.
- Agents must never have unilateral authority to self-approve destructive host file changes.

---

## 🤝 Contributing

Contributions from fellow AI Engineers, Systems Programmers, and ML Researchers are welcome! See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines on code style, typing, and architectural consistency.

---

## 📜 License

Distributed under the MIT License. See [LICENSE](LICENSE) for details.
