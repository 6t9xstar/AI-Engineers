"""
Production ReAct (Reason + Act) Autonomous Agent Loop
Author: 6t9xstar (AI-Engineers)
License: MIT

Demonstrates an end-to-end autonomous agent loop with explicit Thought, Action,
Observation, and Reflection cycles without third-party framework dependencies.
"""

import re
from typing import Callable, Dict, Any, List

class Tool:
    def __init__(self, name: str, func: Callable[[str], str], description: str):
        self.name = name
        self.func = func
        self.description = description

    def execute(self, arg: str) -> str:
        try:
            return self.func(arg)
        except Exception as e:
            return f"Error executing {self.name}: {e}"

# Sample Tools
def tool_search(query: str) -> str:
    knowledge = {
        "shadowcli": "ShadowCLI is a zero-trust CLI sandbox that enforces Landlock LSM, unprivileged user namespaces, and CoW overlays.",
        "mcp": "Model Context Protocol is an open standard introduced by Anthropic in 2024 for agent-to-tool JSON-RPC communication.",
        "rrf": "Reciprocal Rank Fusion is an algorithm that fuses rankings from dense vector and sparse lexical search."
    }
    for k, v in knowledge.items():
        if k in query.lower():
            return v
    return "No matching records found in knowledge base."

def tool_calculator(expr: str) -> str:
    allowed = set("0123456789+-*/(). ")
    if all(c in allowed for c in expr):
        return str(eval(expr, {"__builtins__": None}, {}))
    return "Invalid mathematical expression."

class MockLLM:
    """Simulates an LLM producing ReAct structured reasoning traces."""
    def __init__(self):
        self.turn = 0

    def generate(self, prompt: str) -> str:
        self.turn += 1
        if "calculate" in prompt.lower() and self.turn == 1:
            return "Thought: I need to calculate the value of (1024 - 252) * 2.\nAction: calculator: (1024 - 252) * 2"
        elif "shadowcli" in prompt.lower() and self.turn == 1:
            return "Thought: The user is asking about ShadowCLI. I will query the search tool.\nAction: search: shadowcli"
        elif self.turn == 2:
            return "Thought: I have obtained the necessary observation to answer the user.\nFinal Answer: ShadowCLI provides zero-trust kernel sandboxing for AI coding agents using Linux Landlock LSM and ephemeral Copy-on-Write overlays."
        return "Final Answer: Task complete."

class ReActAgent:
    def __init__(self, tools: List[Tool], llm: MockLLM, max_turns: int = 5):
        self.tools: Dict[str, Tool] = {t.name: t for t in tools}
        self.llm = llm
        self.max_turns = max_turns

    def run(self, user_prompt: str) -> str:
        scratchpad = f"User: {user_prompt}\n"
        print(f"=== Starting ReAct Agent ===")
        print(f"Goal: {user_prompt}\n")

        for turn in range(1, self.max_turns + 1):
            llm_output = self.llm.generate(scratchpad)
            print(f"[Turn {turn}] Model Response:\n{llm_output}\n")

            if "Final Answer:" in llm_output:
                return llm_output.split("Final Answer:")[1].strip()

            action_match = re.search(r"Action:\s*(\w+):\s*(.+)", llm_output)
            if action_match:
                tool_name, tool_arg = action_match.group(1).strip(), action_match.group(2).strip()
                if tool_name in self.tools:
                    obs = self.tools[tool_name].execute(tool_arg)
                else:
                    obs = f"Tool '{tool_name}' not available. Available: {list(self.tools.keys())}"
                
                print(f"-> Observation from '{tool_name}': {obs}\n")
                scratchpad += f"{llm_output}\nObservation: {obs}\n"
            else:
                scratchpad += f"{llm_output}\n"

        return "Agent reached maximum execution depth without completing."

if __name__ == "__main__":
    tools = [
        Tool("search", tool_search, "Search the technical knowledge base"),
        Tool("calculator", tool_calculator, "Evaluate mathematical expressions")
    ]
    agent = ReActAgent(tools=tools, llm=MockLLM())
    answer = agent.run("What security model does ShadowCLI enforce?")
    print(f"=== Final Agent Result ===\n{answer}")
