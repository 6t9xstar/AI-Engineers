# 03: Autonomous Agent Patterns & Workflows

An LLM becomes an **Agent** when it is placed inside a closed-loop execution harness equipped with memory, planning, tools, and reflection.

---

## 1. Core Architectural Archetypes

```
           +---------------------------------------------+
           |                USER GOAL                    |
           +---------------------------------------------+
                                  |
                                  v
+-------------------------------------------------------------------+
|                        THE AGENT LOOP                             |
|                                                                   |
|   +----------------+     +---------------+     +--------------+   |
|   | 1. Thought     | --> | 2. Tool Call  | --> | 3. Execute   |   |
|   | (Reasoning)    |     | (Action)      |     | (In Kernel)  |   |
|   +----------------+     +---------------+     +--------------+   |
|           ^                                           |           |
|           |                                           v           |
|   +----------------+                         +----------------+   |
|   | 5. Reflection  | <---------------------- | 4. Observation |   |
|   | (Evaluation)   |                         | (Result/Stderr)|   |
|   +----------------+                         +----------------+   |
+-------------------------------------------------------------------+
```

---

## 2. The Four Fundamental Agent Patterns

### 1. ReAct (Reason + Act)
Pioneered by Yao et al. (2022). Interleaves explicit reasoning traces with action execution:
- **Thought**: *"I need to check why `test_auth` failed. I should read the test log."*
- **Action**: `read_file(path="test.log")`
- **Observation**: `AssertionError: Expected 200, Got 401 Unauthorized`
- **Thought**: *"The token expired. I will refresh credentials and rerun."*

### 2. Plan-and-Solve (Decomposition)
Separates architectural strategy from tactical tool execution:
1. **Planner LLM**: Decomposes the user request into an explicit directed acyclic graph (DAG) of sub-tasks.
2. **Executor LLM**: Executes each task sequentially or concurrently using tools.
3. **Re-planner**: Dynamically updates the plan if an intermediate step fails or yields surprising findings.

### 3. Reflexion & Self-Correction
When a tool call returns an error or test assertion fails:
- Do not blindly retry the same command.
- Feed the error trace into a **Reflexion Prompt**:
  > *"Your previous attempt failed with: `EACCES Permission denied`. Analyze the root cause, explain your mistake, and generate a revised action."*

### 4. Hierarchical Multi-Agent Supervisors
Single agents struggle with broad scope. Hierarchical teams divide labor by domain:

```
                  +---------------------------+
                  |     SUPERVISOR AGENT      |
                  | (Routes Tasks & Reviews)  |
                  +---------------------------+
                     /          |          \
                    /           |           \
                   v            v            v
           +-----------+  +-----------+  +-----------+
           | Research  |  |  Coding   |  | Testing & |
           |   Agent   |  |   Agent   |  | QA Agent  |
           +-----------+  +-----------+  +-----------+
```

---

## 3. Production Failure Modes & Defenses

1. **Infinite Execution Loops**: Set strict recursion depth limits (`max_turns = 15`) and token budgets.
2. **Tool Hallucination**: Enforce rigid JSON Schema tool validation using Instructor/Pydantic.
3. **Context Poisoning**: Strip verbose terminal dumps (e.g. 5,000 lines of node_modules warnings) down to relevant error lines before feeding back into the prompt.

---

## Next Steps
Proceed to [04: The Model Context Protocol (MCP) Standard](04_mcp_standard.md).
