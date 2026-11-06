# 04: The Model Context Protocol (MCP) Standard

The **Model Context Protocol (MCP)**, introduced by Anthropic in late 2024, is the universal open standard for securely connecting AI models, IDEs, and agent harnesses to external tools, data sources, and execution environments.

---

## 1. Why MCP Replaced Ad-Hoc Tool Calling

Before MCP, every developer platform created proprietary tool formats:
- OpenAI Function Calling schemas
- LangChain Tool classes
- Custom REST endpoints

MCP standardizes tool communication using a bi-directional **JSON-RPC 2.0 protocol** operating over **STDIO** (standard input/output) or **Server-Sent Events (SSE)**.

```
+--------------------+                       +--------------------+
|     MCP HOST       |   JSON-RPC 2.0 (STDIO)|     MCP SERVER     |
| (Claude Code, IDE, | --------------------> | (Filesystem, DB,   |
|   Agent Harness)   | <-------------------- |   CLI Sandboxes)   |
+--------------------+                       +--------------------+
```

---

## 2. Core Protocol Lifecycle

### 1. Initialization (`initialize`)
The client negotiates protocol version and capabilities with the server:

```json
// Client -> Server
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "initialize",
  "params": {
    "protocolVersion": "2024-11-05",
    "capabilities": {},
    "clientInfo": { "name": "claude-code", "version": "1.0.0" }
  }
}
```

### 2. Tool Discovery (`tools/list`)
The server advertises available tools and their strict JSON schemas:

```json
// Server -> Client
{
  "jsonrpc": "2.0",
  "id": 2,
  "result": {
    "tools": [
      {
        "name": "shadow_run",
        "description": "Execute a shell command inside a zero-trust Copy-on-Write sandbox",
        "inputSchema": {
          "type": "object",
          "properties": {
            "command": { "type": "string", "description": "Command to run" }
          },
          "required": ["command"]
        }
      }
    ]
  }
}
```

### 3. Tool Execution (`tools/call`)
The client dispatches tool execution:

```json
// Client -> Server
{
  "jsonrpc": "2.0",
  "id": 3,
  "method": "tools/call",
  "params": {
    "name": "shadow_run",
    "arguments": { "command": "cargo test" }
  }
}
```

---

## 3. Designing Secure MCP Servers

1. **STDIO Discipline**: All server logging, debugging, and diagnostics **MUST** be written strictly to `stderr`. Writing plain text to `stdout` breaks JSON-RPC framing and crashes the client.
2. **Deterministic Error Reporting**: Non-fatal execution errors should be returned with `isError: true` inside a normal tool result response rather than raising a protocol-level JSON-RPC error.
3. **No Unilateral Self-Approval**: Sensitive mutations (like applying staged diffs to production files) must never be exposed as an automatic MCP tool that an LLM can trigger without human approval.

---

## Next Steps
Proceed to [05: Evaluations, Guardrails & LLM-as-a-Judge](05_guardrails_evals.md).
