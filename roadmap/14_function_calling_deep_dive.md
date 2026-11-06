# 14: Function Calling & Constrained Decoding

How LLMs reliably emit machine-executable syntax.

## Constrained Grammar Decoding
Instead of allowing free-form token sampling:
1. Define a Context-Free Grammar (CFG) or JSON Schema.
2. At every generation step, mask model logits for tokens that violate the grammar state machine.
3. Guarantees 100% syntactically valid JSON output with zero parse failures.
