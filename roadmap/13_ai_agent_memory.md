# 13: Agent Memory Architectures & Cognitive State

Autonomous agents need persistent state beyond raw prompt windows.

## Memory Taxonomies

### 1. Working Memory
- Scratchpad state, current plan DAG, and tool call traces within the current execution turn.
- Ephemeral; resets after task resolution.

### 2. Episodic Memory
- Semantic logs of past interactions, user preferences, and previous solution attempts.
- Stored in a vector database and retrieved via similarity when related tasks recur.

### 3. Procedural Memory
- Compiled system instructions, tool schemas, and reusable execution scripts.
