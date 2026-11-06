"""
LLM-as-a-Judge Evaluation Pipeline & Rubric Scorer
Author: 6t9xstar (AI-Engineers)
License: MIT

Demonstrates automated multi-metric evaluation of LLM candidate answers
across Faithfulness (Groundedness) and Answer Relevance.
"""

from typing import Dict, Any, List
from dataclasses import dataclass

@dataclass
class EvalSample:
    query: str
    retrieved_context: str
    generated_answer: str

@dataclass
class EvalResult:
    faithfulness_score: float  # 1.0 to 5.0
    relevance_score: float     # 1.0 to 5.0
    verdict: str
    reasoning: str

class MockJudgeLLM:
    """Simulates an LLM Judge applying an explicit Chain-of-Thought scoring rubric."""
    def judge(self, sample: EvalSample) -> EvalResult:
        # Check if generated answer matches context claims
        words_in_context = set(sample.retrieved_context.lower().split())
        answer_words = set(sample.generated_answer.lower().split())
        overlap = len(words_in_context.intersection(answer_words)) / max(len(answer_words), 1)

        faithfulness = 5.0 if overlap > 0.4 else 2.5
        relevance = 5.0 if any(q in sample.generated_answer.lower() for q in sample.query.lower().split()[:2]) else 3.0

        verdict = "PASS" if faithfulness >= 4.0 and relevance >= 4.0 else "FAIL"
        reasoning = f"Context overlap ratio: {overlap:.2f}. Query terms directly addressed in generated output."

        return EvalResult(
            faithfulness_score=faithfulness,
            relevance_score=relevance,
            verdict=verdict,
            reasoning=reasoning
        )

def run_eval_suite(samples: List[EvalSample]) -> None:
    judge = MockJudgeLLM()
    print("=== Running LLM-as-a-Judge Evaluation Suite ===\n")

    for i, s in enumerate(samples, 1):
        res = judge.judge(s)
        print(f"[Sample #{i}] Query: {s.query}")
        print(f"  Verdict:      {res.verdict}")
        print(f"  Faithfulness: {res.faithfulness_score}/5.0")
        print(f"  Relevance:    {res.relevance_score}/5.0")
        print(f"  Reasoning:    {res.reasoning}\n")

if __name__ == "__main__":
    test_samples = [
        EvalSample(
            query="How does ShadowCLI protect the host filesystem?",
            retrieved_context="ShadowCLI uses Linux user namespaces and Landlock LSM to isolate file operations inside an ephemeral Copy-on-Write upper directory.",
            generated_answer="ShadowCLI protects the host filesystem through Linux user namespaces, Landlock LSM, and Copy-on-Write ephemeral staging."
        ),
        EvalSample(
            query="What is the capital of France?",
            retrieved_context="Paris is the capital and most populous city of France.",
            generated_answer="The capital of France is Berlin, Germany."  # Hallucination sample
        )
    ]
    run_eval_suite(test_samples)
