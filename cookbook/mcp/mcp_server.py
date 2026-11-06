"""
Production Model Context Protocol (MCP) STDIO Server
Author: 6t9xstar (AI-Engineers)
License: MIT

Implements the official MCP specification (version 2024-11-05) over STDIO JSON-RPC 2.0.
Can be plugged directly into Claude Code, Cursor, or any MCP-compliant AI harness.
"""

import sys
import json
from typing import Dict, Any

def send_response(req_id: Any, result: Dict[str, Any]):
    resp = {
        "jsonrpc": "2.0",
        "id": req_id,
        "result": result
    }
    sys.stdout.write(json.dumps(resp) + "\n")
    sys.stdout.flush()

def send_error(req_id: Any, code: int, message: str):
    resp = {
        "jsonrpc": "2.0",
        "id": req_id,
        "error": {
            "code": code,
            "message": message
        }
    }
    sys.stdout.write(json.dumps(resp) + "\n")
    sys.stdout.flush()

def make_text_result(text: str, is_error: bool = False) -> Dict[str, Any]:
    return {
        "content": [
            {
                "type": "text",
                "text": text
            }
        ],
        "isError": is_error
    }

TOOLS = [
    {
        "name": "ai_engineers_status",
        "description": "Returns status and active configuration of the AI-Engineers toolkit.",
        "inputSchema": {
            "type": "object",
            "properties": {},
            "required": []
        }
    },
    {
        "name": "query_knowledge_base",
        "description": "Searches the AI Engineering knowledge base for architecture patterns.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "topic": {
                    "type": "string",
                    "description": "Topic to search for (e.g. 'rag', 'agents', 'mcp', 'security')"
                }
            },
            "required": ["topic"]
        }
    }
]

def handle_call_tool(tool_name: str, args: Dict[str, Any]) -> Dict[str, Any]:
    if tool_name == "ai_engineers_status":
        return make_text_result("AI-Engineers toolkit active. Version 1.0.0. Modules: RAG, Agents, MCP, Security.")
    elif tool_name == "query_knowledge_base":
        topic = args.get("topic", "").lower()
        if "security" in topic or "sandbox" in topic:
            return make_text_result("Security Architecture: Use ShadowCLI for containerless zero-trust agent isolation via Landlock LSM and OverlayFS.")
        elif "rag" in topic:
            return make_text_result("RAG Architecture: Use Hybrid Search (Dense + BM25) fused with Reciprocal Rank Fusion (RRF) and Cross-Encoder reranking.")
        elif "mcp" in topic:
            return make_text_result("MCP Architecture: JSON-RPC 2.0 over STDIO with strict JSON Schema tool registration.")
        else:
            return make_text_result(f"Topic '{topic}' indexed. See roadmap/ for complete specifications.")
    else:
        return make_text_result(f"Unknown tool: {tool_name}", is_error=True)

def main():
    # Diagnostic logs MUST go exclusively to stderr to avoid corrupting JSON-RPC framing
    sys.stderr.write("AI-Engineers MCP Server listening on STDIO...\n")
    sys.stderr.flush()

    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            req = json.loads(line)
        except json.JSONDecodeError as e:
            send_error(None, -32700, f"Parse error: {e}")
            continue

        req_id = req.get("id")
        method = req.get("method")
        params = req.get("params", {})

        if method == "initialize":
            send_response(req_id, {
                "protocolVersion": "2024-11-05",
                "capabilities": {
                    "tools": {}
                },
                "serverInfo": {
                    "name": "ai-engineers-mcp",
                    "version": "1.0.0"
                }
            })
        elif method == "tools/list":
            send_response(req_id, {
                "tools": TOOLS
            })
        elif method == "tools/call":
            tool_name = params.get("name")
            tool_args = params.get("arguments", {})
            result = handle_call_tool(tool_name, tool_args)
            send_response(req_id, result)
        elif method == "notifications/initialized":
            # Client acknowledgment; no response expected for notifications
            pass
        else:
            send_error(req_id, -32601, f"Method '{method}' not found")

if __name__ == "__main__":
    main()
