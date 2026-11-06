"""
Deterministic Structured Outputs & Self-Correction Feedback Loop
Author: 6t9xstar (AI-Engineers)
License: MIT

Demonstrates schema-enforced JSON generation with programmatic validation
and automated error feedback correction loops without hard failures.
"""

import json
from dataclasses import dataclass, asdict
from typing import List, Optional, Dict, Any

@dataclass
class ArchitectureSpec:
    system_name: str
    target_environment: str
    components: List[str]
    max_memory_mb: int
    security_sandboxed: bool

    def validate(self) -> List[str]:
        errors = []
        if not self.system_name or len(self.system_name) < 3:
            errors.append("system_name must be at least 3 characters.")
        if self.target_environment not in ["production", "staging", "development"]:
            errors.append("target_environment must be one of: production, staging, development.")
        if not self.components or len(self.components) == 0:
            errors.append("components must contain at least one module.")
        if self.max_memory_mb < 128:
            errors.append("max_memory_mb must be >= 128 MB.")
        return errors

class SchemaExtractor:
    """Simulates an LLM extraction pipeline with self-correcting validation."""
    def __init__(self):
        self.attempts = 0

    def parse_with_retry(self, raw_input: str, max_retries: int = 3) -> ArchitectureSpec:
        feedback = ""
        for attempt in range(1, max_retries + 1):
            print(f"[Attempt {attempt}] Requesting structured extraction...")
            # Simulate first attempt returning invalid environment, second fixing it
            if attempt == 1:
                candidate_json = {
                    "system_name": "ShadowSandbox",
                    "target_environment": "prod",  # Invalid (must be 'production')
                    "components": ["Landlock", "Seccomp", "OverlayFS"],
                    "max_memory_mb": 512,
                    "security_sandboxed": True
                }
            else:
                candidate_json = {
                    "system_name": "ShadowSandbox",
                    "target_environment": "production",  # Corrected
                    "components": ["Landlock", "Seccomp", "OverlayFS"],
                    "max_memory_mb": 512,
                    "security_sandboxed": True
                }

            spec = ArchitectureSpec(**candidate_json)
            validation_errors = spec.validate()

            if not validation_errors:
                print(f"[Attempt {attempt}] Schema validated cleanly!\n")
                return spec
            else:
                feedback = f"Validation failed with errors: {'; '.join(validation_errors)}"
                print(f"-> {feedback}")
                print(f"-> Sending feedback back into LLM error-correction prompt...\n")

        raise ValueError("Failed to extract valid schema within retry limit.")

if __name__ == "__main__":
    extractor = SchemaExtractor()
    spec = extractor.parse_with_retry("Set up ShadowSandbox in production with Landlock, Seccomp, and OverlayFS using 512MB RAM.")
    print("=== Extracted Specification Object ===")
    print(json.dumps(asdict(spec), indent=2))
