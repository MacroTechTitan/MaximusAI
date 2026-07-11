"""
eval-harness.py
---------------
RAG evaluation harness measuring:
  1. Retrieval recall@k  — did the top-k chunks include the known-relevant chunk?
  2. Answer faithfulness — is each claim in the answer supported by cited chunks?
  3. Answer correctness  — does the answer match the golden answer?

Faithfulness is measured using an LLM judge (gpt-4o-mini at temperature=0).
Correctness uses exact-match for simple cases and LLM judge for complex cases.

Requirements:
    pip install openai psycopg2-binary sentence-transformers numpy

Environment:
    OPENAI_API_KEY, DATABASE_URL

Usage:
    python eval-harness.py
"""

import os
import json
import time
from dataclasses import dataclass, field
from typing import Optional
from openai import OpenAI

# Import the retrieval functions from the pipeline
# In a real project these would be in a shared module
# Here we define stubs and note where to import from
try:
    from pgvector_setup import retrieve_hybrid, generate_answer
except ImportError:
    print("[warn] pgvector_setup not found — using stub functions for demonstration")
    def retrieve_hybrid(query, top_k=5):
        return []
    def generate_answer(query, chunks):
        return {"answer": "", "cited_chunks": []}

client = OpenAI()

# ---------------------------------------------------------------------------
# Golden eval set
# ---------------------------------------------------------------------------
@dataclass
class EvalCase:
    id: str
    question: str
    golden_answer: str          # expected correct answer (for correctness check)
    relevant_doc_ids: list      # doc IDs that must appear in top-k for recall@k
    answerable: bool = True     # False = unanswerable; expect "I don't know" style response
    tags: list = field(default_factory=list)

EVAL_CASES = [
    EvalCase(
        id="eval-001",
        question="What does the Pro plan include?",
        golden_answer="The Pro plan costs $99/month and includes unlimited users, 100GB storage, priority support, and API access.",
        relevant_doc_ids=["doc-001"],
        tags=["factual-lookup"],
    ),
    EvalCase(
        id="eval-002",
        question="How do I request a refund for an annual plan?",
        golden_answer="Contact billing@example.com with your account email and order number. Refunds are prorated for unused months.",
        relevant_doc_ids=["doc-002"],
        tags=["procedural"],
    ),
    EvalCase(
        id="eval-003",
        question="Can I get a refund for API usage charges?",
        golden_answer="No, usage-based charges are non-refundable.",
        relevant_doc_ids=["doc-002"],
        tags=["factual-lookup"],
    ),
    EvalCase(
        id="eval-004",
        question="What is the capital of France?",
        golden_answer="I don't have information about that in the available documents.",
        relevant_doc_ids=[],
        answerable=False,
        tags=["unanswerable"],
    ),
    EvalCase(
        id="eval-005",
        question="How much does the Basic plan cost per month?",
        golden_answer="The Basic plan costs $29/month.",
        relevant_doc_ids=["doc-001"],
        tags=["factual-lookup"],
    ),
]


# ---------------------------------------------------------------------------
# Metric: Retrieval Recall@k
# ---------------------------------------------------------------------------
def measure_recall_at_k(retrieved_chunks: list[dict], relevant_doc_ids: list, k: int = 5) -> float:
    """
    Did any of the top-k retrieved chunks come from a relevant document?
    Returns 1.0 if yes, 0.0 if no.
    For multi-doc cases, returns fraction of relevant docs found.
    """
    if not relevant_doc_ids:
        return 1.0  # unanswerable case — no relevant docs to find
    retrieved_doc_ids = {c["doc_id"] for c in retrieved_chunks[:k]}
    found = sum(1 for doc_id in relevant_doc_ids if doc_id in retrieved_doc_ids)
    return found / len(relevant_doc_ids)


# ---------------------------------------------------------------------------
# Metric: Answer Faithfulness (LLM judge)
# ---------------------------------------------------------------------------
FAITHFULNESS_PROMPT = """You are an evaluation assistant.

You will be given an answer and the context chunks it was supposedly based on.
Your task: determine if every factual claim in the answer is supported by the context.

Answer to evaluate:
{answer}

Context chunks:
{context}

Respond with a JSON object:
{{
  "faithfulness_score": <float 0.0-1.0>,
  "unsupported_claims": [<list of any claims not in context, or empty list>],
  "reasoning": "<one sentence>"
}}
"""

def measure_faithfulness(answer: str, cited_chunks: list[dict]) -> dict:
    """Use GPT-4o-mini as a faithfulness judge."""
    if not answer or "don't have information" in answer.lower():
        return {"faithfulness_score": 1.0, "unsupported_claims": [], "reasoning": "Abstained appropriately."}

    context = "\n\n".join(f"[{c.get('id', 'chunk')}]: {c['body']}" for c in cited_chunks)
    if not context:
        return {"faithfulness_score": 0.0, "unsupported_claims": [answer], "reasoning": "No context provided to judge against."}

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        temperature=0,
        messages=[
            {"role": "user", "content": FAITHFULNESS_PROMPT.format(answer=answer, context=context)}
        ],
        response_format={"type": "json_object"}
    )
    return json.loads(response.choices[0].message.content)


# ---------------------------------------------------------------------------
# Metric: Answer Correctness (LLM judge)
# ---------------------------------------------------------------------------
CORRECTNESS_PROMPT = """You are an evaluation assistant.

Compare the system answer to the golden answer. Determine if the system answer is correct.
Minor paraphrasing is fine; do not penalise for different wording if the meaning is the same.
Penalise for missing key facts or stating incorrect facts.

System answer: {system_answer}
Golden answer: {golden_answer}

Respond with JSON:
{{
  "correct": <true or false>,
  "score": <float 0.0-1.0>,
  "reasoning": "<one sentence>"
}}
"""

def measure_correctness(system_answer: str, golden_answer: str) -> dict:
    """Use GPT-4o-mini as a correctness judge."""
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        temperature=0,
        messages=[
            {"role": "user", "content": CORRECTNESS_PROMPT.format(
                system_answer=system_answer, golden_answer=golden_answer
            )}
        ],
        response_format={"type": "json_object"}
    )
    return json.loads(response.choices[0].message.content)


# ---------------------------------------------------------------------------
# Run evaluation
# ---------------------------------------------------------------------------
@dataclass
class EvalResult:
    case_id: str
    question: str
    tags: list
    recall_at_5: float
    faithfulness: float
    correctness: float
    answer: str
    latency_ms: float


def run_eval(cases: list[EvalCase], verbose: bool = True) -> list[EvalResult]:
    results = []
    for case in cases:
        if verbose:
            print(f"\n[{case.id}] {case.question[:70]}...")

        t0 = time.time()
        chunks = retrieve_hybrid(case.question, top_k=5)
        gen_result = generate_answer(case.question, chunks)
        latency_ms = (time.time() - t0) * 1000

        answer = gen_result["answer"]
        cited_chunks = gen_result.get("cited_chunks", chunks)

        recall = measure_recall_at_k(chunks, case.relevant_doc_ids, k=5)
        faith = measure_faithfulness(answer, cited_chunks)
        correct = measure_correctness(answer, case.golden_answer)

        result = EvalResult(
            case_id=case.id,
            question=case.question,
            tags=case.tags,
            recall_at_5=recall,
            faithfulness=faith["faithfulness_score"],
            correctness=correct["score"],
            answer=answer[:120],
            latency_ms=latency_ms,
        )
        results.append(result)

        if verbose:
            print(f"  Recall@5: {recall:.2f} | Faithfulness: {faith['faithfulness_score']:.2f} | Correctness: {correct['score']:.2f} | Latency: {latency_ms:.0f}ms")

    return results


def print_summary(results: list[EvalResult]):
    """Print aggregate metrics."""
    n = len(results)
    avg_recall = sum(r.recall_at_5 for r in results) / n
    avg_faith = sum(r.faithfulness for r in results) / n
    avg_correct = sum(r.correctness for r in results) / n
    avg_latency = sum(r.latency_ms for r in results) / n

    print("\n" + "=" * 60)
    print("EVAL SUMMARY")
    print("=" * 60)
    print(f"Cases evaluated:   {n}")
    print(f"Recall@5:          {avg_recall:.3f}  (target: ≥ 0.80)")
    print(f"Faithfulness:      {avg_faith:.3f}  (target: ≥ 0.95)")
    print(f"Correctness:       {avg_correct:.3f}  (target: ≥ 0.80)")
    print(f"Avg latency:       {avg_latency:.0f}ms")
    print()

    # Failures
    failures = [r for r in results if r.recall_at_5 < 0.5 or r.faithfulness < 0.8 or r.correctness < 0.5]
    if failures:
        print(f"FAILURES ({len(failures)}):")
        for f in failures:
            print(f"  [{f.case_id}] recall={f.recall_at_5:.2f} faith={f.faithfulness:.2f} correct={f.correctness:.2f}")
    else:
        print("All cases passed thresholds.")

    # Save results
    output_path = "eval_results.json"
    with open(output_path, "w") as fh:
        json.dump(
            [{"case_id": r.case_id, "recall_at_5": r.recall_at_5,
              "faithfulness": r.faithfulness, "correctness": r.correctness,
              "latency_ms": r.latency_ms} for r in results],
            fh, indent=2
        )
    print(f"\nResults saved to {output_path}")


if __name__ == "__main__":
    print("Running RAG evaluation harness...")
    results = run_eval(EVAL_CASES, verbose=True)
    print_summary(results)
