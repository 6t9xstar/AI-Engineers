#!/usr/bin/env python3
"""
AI-Engineers Interactive CLI & Developer Toolkit (2026)
Author: 6t9xstar (https://github.com/6t9xstar/AI-Engineers)
License: MIT

Zero-dependency CLI utility for searching the handbook, scaffolding agent projects,
running cookbook recipes, and launching the Model Context Protocol (MCP) server.
"""

import sys
import os
import argparse
import subprocess
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

def cmd_search(query: str):
    """Searches the entire handbook, roadmaps, papers, and glossary for a query."""
    print(f"\n[SEARCH] AI-Engineers Knowledge Base: '{query}'\n" + "=" * 65)
    from cookbook.rag.hybrid_search import SimpleBM25

    indexed_docs = []
    file_map = []

    search_dirs = ["roadmap", "papers", "cheat_sheets", "glossary/terms", "cookbook"]
    for s_dir in search_dirs:
        dir_path = ROOT_DIR / s_dir
        if not dir_path.exists():
            continue
        for ext in ("*.md", "*.py"):
            for file_path in dir_path.rglob(ext):
                try:
                    text = file_path.read_text(encoding="utf-8")
                    indexed_docs.append(text[:2000])  # First 2000 chars
                    file_map.append(file_path.relative_to(ROOT_DIR))
                except Exception:
                    pass

    if not indexed_docs:
        print("No documents found in knowledge base.")
        return

    bm25 = SimpleBM25(indexed_docs)
    results = bm25.score(query)

    found = 0
    for doc_idx, score in results[:5]:
        if score > 0.05:
            found += 1
            rel_file = file_map[doc_idx]
            first_line = indexed_docs[doc_idx].strip().split("\n")[0].replace("#", "").strip()
            print(f"[{score:.3f}] {rel_file}")
            print(f"       -> {first_line}")

    if found == 0:
        print("No exact matches found. Try searching for broader terms like 'rag', 'mcp', 'landlock', 'lora'.")
    print("=" * 65 + "\n")

def cmd_test():
    """Runs all cookbook recipes to verify execution integrity."""
    print("\n[TEST] Running AI-Engineers Verification Suite...\n" + "=" * 65)
    cookbooks = [
        "cookbook/rag/hybrid_search.py",
        "cookbook/agents/react_agent.py",
        "cookbook/structured_outputs/instructor_pydantic.py",
        "cookbook/evals/llm_as_judge.py",
    ]

    passed = 0
    for rel_path in cookbooks:
        full_path = ROOT_DIR / rel_path
        sys.stdout.write(f"Testing {rel_path} ... ")
        sys.stdout.flush()
        res = subprocess.run([sys.executable, str(full_path)], capture_output=True, text=True)
        if res.returncode == 0:
            print("[OK] PASSED")
            passed += 1
        else:
            print("[FAIL] FAILED")
            print(res.stderr)

    print(f"\nResult: {passed}/{len(cookbooks)} cookbooks verified cleanly.\n" + "=" * 65)

def cmd_scaffold(template: str, name: str):
    """Scaffolds a production-ready template."""
    dest = Path.cwd() / name
    if dest.exists():
        print(f"Error: Directory '{name}' already exists.")
        return

    dest.mkdir(parents=True)
    if template.lower() == "rag":
        src = ROOT_DIR / "cookbook" / "rag" / "hybrid_search.py"
        (dest / "main.py").write_text(src.read_text(encoding="utf-8"), encoding="utf-8")
        print(f"[OK] Scaffolded Production RAG project in ./{name}/")
    elif template.lower() == "agent":
        src = ROOT_DIR / "cookbook" / "agents" / "react_agent.py"
        (dest / "main.py").write_text(src.read_text(encoding="utf-8"), encoding="utf-8")
        print(f"[OK] Scaffolded Autonomous ReAct Agent project in ./{name}/")
    elif template.lower() == "mcp":
        src = ROOT_DIR / "cookbook" / "mcp" / "mcp_server.py"
        (dest / "server.py").write_text(src.read_text(encoding="utf-8"), encoding="utf-8")
        print(f"[OK] Scaffolded Model Context Protocol (MCP) Server in ./{name}/")
    else:
        print(f"Unknown template '{template}'. Available: rag, agent, mcp")

def cmd_mcp():
    """Starts the Model Context Protocol (MCP) server."""
    mcp_script = ROOT_DIR / "cookbook" / "mcp" / "mcp_server.py"
    subprocess.run([sys.executable, str(mcp_script)])

def main():
    parser = argparse.ArgumentParser(
        description="AI-Engineers Toolkit CLI: Search, test, and scaffold production AI systems."
    )
    subparsers = parser.add_subparsers(dest="command")

    # Search
    search_parser = subparsers.add_parser("search", help="Search the AI-Engineers handbook & code")
    search_parser.add_argument("query", type=str, help="Search query (e.g. 'hybrid search', 'landlock')")

    # Test
    subparsers.add_parser("test", help="Run cookbook test suite")

    # Scaffold
    scaffold_parser = subparsers.add_parser("scaffold", help="Scaffold a starter project")
    scaffold_parser.add_argument("template", choices=["rag", "agent", "mcp"], help="Template type")
    scaffold_parser.add_argument("name", type=str, help="Project directory name")

    # MCP
    subparsers.add_parser("mcp", help="Launch the built-in MCP server over STDIO")

    args = parser.parse_args()

    if args.command == "search":
        cmd_search(args.query)
    elif args.command == "test":
        cmd_test()
    elif args.command == "scaffold":
        cmd_scaffold(args.template, args.name)
    elif args.command == "mcp":
        cmd_mcp()
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
