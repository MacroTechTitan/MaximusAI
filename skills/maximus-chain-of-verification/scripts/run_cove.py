#!/usr/bin/env python3
"""Reference runner for maximus-chain-of-verification.

Enforces independent-context isolation for Phase 3 (verification answering).
This is a scaffold — swap the model-call functions for your actual runtime
(Anthropic SDK, OpenAI SDK, Perplexity Computer sub-agent spawner, etc.).

The point of this file: show what "factored CoVe" looks like in code, so a
naive fact-check prompt (draft visible during verification) is impossible.
"""

from __future__ import annotations

import json
import sys
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path


# ---------- Data shapes ----------

@dataclass
class VerificationQuestion:
    q_id: str
    text: str


@dataclass
class Claim:
    claim_id: str
    claim_text: str
    questions: list[VerificationQuestion] = field(default_factory=list)


@dataclass
class VerificationAnswer:
    q_id: str
    claim_id: str
    answer_text: str
    sources: list[dict]
    confidence: str  # high | medium | low | cannot_confirm


# ---------- Phase 2: question generation ----------

def generate_verification_questions(draft: str) -> list[Claim]:
    """Extract verifiable claims and generate 1–3 questions per claim.

    Replace the body with a real model call. Prompt should include:
    - 'Return only claims with checkable facts (numbers, dates, names, quotes,
      benchmark scores, attributions). Skip opinions and framing.'
    - 'For each claim generate 1–3 neutral, atomic questions answerable
      WITHOUT the draft in context.'
    - Return JSON matching the Claim schema above.
    """
    raise NotImplementedError(
        "Wire this to your model. Return list[Claim]. See references/output-format.md."
    )


# ---------- Phase 3: independent-context answering ----------

def answer_in_isolation(question: VerificationQuestion) -> VerificationAnswer:
    """Answer ONE verification question in a FRESH context.

    The critical rule: the draft MUST NOT be visible when this runs.
    Recommended implementation: spawn a sub-agent per question so the parent
    conversation's draft cannot leak in.

    Prompt should include:
    - The question and nothing else about the draft.
    - Instruction to search / fetch fresh sources; do not rely on memory.
    - 'If no independent source can be found, answer "Cannot confirm."'
    - Return JSON matching the VerificationAnswer schema.
    """
    raise NotImplementedError(
        "Spawn a fresh sub-agent per question. Do NOT pass the draft. "
        "Return a VerificationAnswer."
    )


def run_phase_3(claims: list[Claim]) -> list[VerificationAnswer]:
    """Iterate claims × questions with strict context isolation."""
    answers: list[VerificationAnswer] = []
    for claim in claims:
        for q in claim.questions:
            # Each call spawns a fresh sub-agent. The draft is not passed in.
            ans = answer_in_isolation(q)
            answers.append(ans)
    return answers


# ---------- Phase 4: revision ----------

def revise_draft(draft: str, claims: list[Claim], answers: list[VerificationAnswer]) -> tuple[str, list[dict]]:
    """Merge verification answers back into the draft.

    Returns:
        revised_draft: Markdown text with corrections applied
        ledger: list of dicts with per-claim {claim, question, verified_answer,
                source, confidence, action}
    """
    raise NotImplementedError(
        "Model call. Prompt: 'Revise the draft so every claim matches the "
        "verification answers. Cut claims with confidence=cannot_confirm. "
        "Soften claims with confidence=low. For each material change, produce "
        "a ledger entry.'"
    )


# ---------- Orchestration ----------

def run_cove(draft: str, out_dir: Path) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    now = datetime.now(timezone.utc).isoformat()

    # Phase 2
    claims = generate_verification_questions(draft)
    (out_dir / "verification-questions.json").write_text(
        json.dumps({"generated_at": now, "claims": [c.__dict__ for c in claims]}, indent=2, default=str)
    )

    # Phase 3 — fresh context per question
    answers = run_phase_3(claims)
    (out_dir / "verification-answers.json").write_text(
        json.dumps({"answered_at": now, "answers": [a.__dict__ for a in answers]}, indent=2, default=str)
    )

    # Phase 4
    revised, ledger = revise_draft(draft, claims, answers)
    (out_dir / "revised-draft.md").write_text(revised)
    (out_dir / "ledger.json").write_text(json.dumps(ledger, indent=2, default=str))

    print(f"CoVe complete. Outputs in {out_dir}:")
    print("  verification-questions.json")
    print("  verification-answers.json")
    print("  revised-draft.md")
    print("  ledger.json")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: run_cove.py <draft.md> <output_dir>")
        sys.exit(1)
    draft_text = Path(sys.argv[1]).read_text()
    run_cove(draft_text, Path(sys.argv[2]))
