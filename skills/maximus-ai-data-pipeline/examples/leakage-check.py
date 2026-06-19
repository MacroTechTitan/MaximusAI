"""
Train/Val/Test Leakage Detection
==================================
Detects two types of train/test leakage:

1. Exact ID leakage: the same example ID appears in multiple splits.
2. Near-duplicate leakage: an example in test/val is semantically very similar
   to an example in train (which inflates benchmark scores).

Usage:
    python leakage-check.py --train data/train.jsonl --val data/val.jsonl --test data/test.jsonl

Outputs:
    - Summary report to stdout
    - Detailed overlap report to leakage_report.json

Install:
    pip install datasketch tqdm
    # For embedding-based dedup: pip install sentence-transformers
"""

import argparse
import json
import hashlib
import logging
from pathlib import Path
from typing import Optional

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")


# ---------------------------------------------------------------------------
# Data loading
# ---------------------------------------------------------------------------

def load_jsonl(path: str) -> list[dict]:
    """Load a JSONL file. Each line must be valid JSON."""
    records = []
    with open(path, "r", encoding="utf-8") as f:
        for i, line in enumerate(f):
            line = line.strip()
            if not line:
                continue
            try:
                records.append(json.loads(line))
            except json.JSONDecodeError as e:
                raise ValueError(f"Invalid JSON on line {i+1} of {path}: {e}") from e
    logger.info("Loaded %d records from %s", len(records), path)
    return records


def extract_text(record: dict) -> str:
    """
    Extract the primary text content from a record.
    Handles common formats: OpenAI Chat JSONL, DPO format, and plain text.
    """
    # OpenAI Chat format: {"messages": [{"role": "user", "content": "..."}]}
    if "messages" in record:
        user_messages = [m["content"] for m in record["messages"] if m.get("role") == "user"]
        return " ".join(user_messages)

    # DPO format: {"prompt": "...", "chosen": "...", "rejected": "..."}
    if "prompt" in record:
        return record["prompt"]

    # Generic: use "text", "input", or "content" keys
    for key in ("text", "input", "content", "question"):
        if key in record:
            return str(record[key])

    # Fallback: serialize the whole record
    return json.dumps(record, ensure_ascii=False)


def extract_id(record: dict, index: int) -> str:
    """Extract or generate a record ID."""
    for key in ("id", "example_id", "row_id", "_id"):
        if key in record:
            return str(record[key])
    return f"idx_{index}"


# ---------------------------------------------------------------------------
# Check 1: Exact ID overlap
# ---------------------------------------------------------------------------

def check_id_overlap(
    splits: dict[str, list[dict]]
) -> dict[str, list[str]]:
    """
    Check for exact ID overlaps between splits.

    Returns a dict mapping split-pair names to lists of overlapping IDs.
    """
    split_ids = {}
    for split_name, records in splits.items():
        split_ids[split_name] = {
            extract_id(r, i) for i, r in enumerate(records)
        }

    overlaps = {}
    split_names = list(split_ids.keys())
    for i in range(len(split_names)):
        for j in range(i + 1, len(split_names)):
            a, b = split_names[i], split_names[j]
            overlap = split_ids[a] & split_ids[b]
            pair_key = f"{a}_vs_{b}"
            overlaps[pair_key] = sorted(overlap)
            if overlap:
                logger.warning(
                    "ID OVERLAP: %d IDs appear in both %s and %s: %s...",
                    len(overlap), a, b, list(overlap)[:3]
                )
            else:
                logger.info("ID overlap check %s vs %s: CLEAN", a, b)

    return overlaps


# ---------------------------------------------------------------------------
# Check 2: Content hash overlap (exact text duplicates)
# ---------------------------------------------------------------------------

def hash_text(text: str) -> str:
    return hashlib.sha256(text.strip().lower().encode("utf-8")).hexdigest()


def check_content_hash_overlap(
    splits: dict[str, list[dict]]
) -> dict[str, list[str]]:
    """
    Check for exact text content duplicates between splits using SHA-256 hashing.
    Faster than MinHash; catches exact duplicates only.
    """
    split_hashes = {}
    for split_name, records in splits.items():
        hashes = {}
        for i, record in enumerate(records):
            text = extract_text(record)
            h = hash_text(text)
            hashes[h] = extract_id(record, i)
        split_hashes[split_name] = hashes

    overlaps = {}
    split_names = list(split_hashes.keys())
    for i in range(len(split_names)):
        for j in range(i + 1, len(split_names)):
            a, b = split_names[i], split_names[j]
            shared_hashes = set(split_hashes[a].keys()) & set(split_hashes[b].keys())
            overlapping_ids = [split_hashes[a][h] for h in shared_hashes]
            pair_key = f"{a}_vs_{b}"
            overlaps[pair_key] = overlapping_ids
            if overlapping_ids:
                logger.warning(
                    "CONTENT DUPLICATE: %d exact-text duplicates between %s and %s",
                    len(overlapping_ids), a, b
                )
            else:
                logger.info("Content hash check %s vs %s: CLEAN", a, b)

    return overlaps


# ---------------------------------------------------------------------------
# Check 3: Near-duplicate detection using MinHash LSH
# ---------------------------------------------------------------------------

def check_near_duplicate_overlap(
    splits: dict[str, list[dict]],
    threshold: float = 0.8,
    num_perm: int = 128,
) -> dict[str, list[tuple[str, str, float]]]:
    """
    Detect near-duplicate (semantically similar) examples across splits using MinHash LSH.

    Args:
        threshold: Jaccard similarity threshold above which two texts are considered near-duplicates.
                   0.8 is a good default for catching near-duplicates while avoiding false positives.
        num_perm: Number of permutations for MinHash. Higher = more accurate, slower.

    Returns:
        Dict mapping split-pair names to lists of (id_a, id_b, similarity_score) tuples.

    Requires: pip install datasketch
    """
    try:
        from datasketch import MinHash, MinHashLSH
    except ImportError:
        logger.warning(
            "datasketch not installed. Skipping near-duplicate check. "
            "Run: pip install datasketch"
        )
        return {}

    def text_to_shingles(text: str, k: int = 3) -> set[str]:
        """Convert text to character k-grams (shingles) for MinHash."""
        text = text.lower().strip()
        return {text[i:i+k] for i in range(len(text) - k + 1)} if len(text) >= k else {text}

    def build_minhash(text: str, num_perm: int) -> "MinHash":
        m = MinHash(num_perm=num_perm)
        for shingle in text_to_shingles(text):
            m.update(shingle.encode("utf8"))
        return m

    all_overlaps = {}
    split_names = list(splits.keys())

    for i in range(len(split_names)):
        for j in range(i + 1, len(split_names)):
            split_a, split_b = split_names[i], split_names[j]
            pair_key = f"{split_a}_vs_{split_b}"

            logger.info("Near-duplicate check: %s vs %s (threshold=%.2f)...", split_a, split_b, threshold)

            lsh = MinHashLSH(threshold=threshold, num_perm=num_perm)

            # Index all records from split_a
            minhashes_a = {}
            for idx, record in enumerate(splits[split_a]):
                record_id = f"{split_a}:{extract_id(record, idx)}"
                text = extract_text(record)
                mh = build_minhash(text, num_perm)
                minhashes_a[record_id] = mh
                lsh.insert(record_id, mh)

            # Query all records from split_b
            near_dups = []
            for idx, record in enumerate(splits[split_b]):
                record_id_b = f"{split_b}:{extract_id(record, idx)}"
                text = extract_text(record)
                mh_b = build_minhash(text, num_perm)
                results = lsh.query(mh_b)
                for record_id_a in results:
                    # Compute exact Jaccard similarity
                    jaccard = minhashes_a[record_id_a].jaccard(mh_b)
                    near_dups.append((record_id_a, record_id_b, round(jaccard, 3)))

            all_overlaps[pair_key] = near_dups
            if near_dups:
                logger.warning(
                    "NEAR-DUPLICATE: %d near-duplicate pairs between %s and %s",
                    len(near_dups), split_a, split_b
                )
            else:
                logger.info("Near-duplicate check %s vs %s: CLEAN", split_a, split_b)

    return all_overlaps


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def run_leakage_check(
    train_path: str,
    val_path: Optional[str] = None,
    test_path: Optional[str] = None,
    near_dup_threshold: float = 0.8,
    output_path: str = "leakage_report.json",
):
    """Run all leakage checks and produce a report."""
    splits = {}
    splits["train"] = load_jsonl(train_path)
    if val_path:
        splits["val"] = load_jsonl(val_path)
    if test_path:
        splits["test"] = load_jsonl(test_path)

    if len(splits) < 2:
        logger.error("Need at least 2 splits to check for leakage.")
        return

    report = {
        "splits": {k: len(v) for k, v in splits.items()},
        "id_overlaps": check_id_overlap(splits),
        "content_hash_overlaps": check_content_hash_overlap(splits),
        "near_duplicate_overlaps": check_near_duplicate_overlap(splits, threshold=near_dup_threshold),
    }

    # Summary
    total_issues = sum(
        len(v) for overlaps in [report["id_overlaps"], report["content_hash_overlaps"]]
        for v in overlaps.values()
    ) + sum(
        len(v) for v in report["near_duplicate_overlaps"].values()
    )

    report["summary"] = {
        "total_issues_found": total_issues,
        "clean": total_issues == 0,
    }

    with open(output_path, "w") as f:
        json.dump(report, f, indent=2)

    print(f"\n{'='*50}")
    print(f"LEAKAGE CHECK SUMMARY")
    print(f"{'='*50}")
    for split_name, count in report["splits"].items():
        print(f"  {split_name}: {count} examples")
    print(f"\nTotal issues found: {total_issues}")
    if total_issues == 0:
        print("RESULT: CLEAN — no leakage detected")
    else:
        print("RESULT: LEAKAGE DETECTED — see leakage_report.json for details")
        print("Action: Remove overlapping examples from train (not from val/test)")
    print(f"\nFull report: {output_path}")

    return report


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Check for train/val/test leakage in ML datasets")
    parser.add_argument("--train", required=True, help="Path to train.jsonl")
    parser.add_argument("--val", default=None, help="Path to val.jsonl")
    parser.add_argument("--test", default=None, help="Path to test.jsonl")
    parser.add_argument("--threshold", type=float, default=0.8,
                        help="Jaccard similarity threshold for near-duplicate detection (default: 0.8)")
    parser.add_argument("--output", default="leakage_report.json",
                        help="Output path for the leakage report JSON")
    args = parser.parse_args()

    run_leakage_check(
        train_path=args.train,
        val_path=args.val,
        test_path=args.test,
        near_dup_threshold=args.threshold,
        output_path=args.output,
    )
