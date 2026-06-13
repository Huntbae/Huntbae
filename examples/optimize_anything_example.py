"""
GEPA 'optimize_anything' example — optimize any text artifact with a custom evaluator.

Useful when you want to optimize things that are not strictly prompts:
    - regex patterns, SQL queries
    - code snippets, config files
    - SVGs or other text artifacts

Run:
    python examples/optimize_anything_example.py
"""

import re

from dotenv import load_dotenv

import gepa.optimize_anything as oa
from gepa.optimize_anything import EngineConfig, GEPAConfig, optimize_anything

load_dotenv()


POSITIVES = [
    "alice@example.com",
    "bob.smith+filter@sub.example.co.kr",
    "x_y-z@a-b.io",
]
NEGATIVES = [
    "not-an-email",
    "@missing-local.com",
    "missing-at.example.com",
    "spaces in@address.com",
]


def evaluate(candidate: str) -> float:
    """Score a candidate regex by F1 on the labeled cases."""
    try:
        pattern = re.compile(candidate.strip())
    except re.error as exc:
        oa.log(f"regex compile error: {exc}")
        return 0.0

    tp = sum(1 for s in POSITIVES if pattern.fullmatch(s))
    fp = sum(1 for s in NEGATIVES if pattern.fullmatch(s))
    fn = len(POSITIVES) - tp

    oa.log(f"TP={tp} FP={fp} FN={fn}")
    if tp + fp == 0 or tp + fn == 0:
        return 0.0
    precision = tp / (tp + fp)
    recall = tp / (tp + fn)
    if precision + recall == 0:
        return 0.0
    return 2 * precision * recall / (precision + recall)


def main() -> None:
    result = optimize_anything(
        seed_candidate=r".+@.+\..+",
        evaluator=evaluate,
        objective=(
            "Produce a Python regex that fullmatches every positive example and "
            "rejects every negative example. Return only the regex, no explanation."
        ),
        config=GEPAConfig(engine=EngineConfig(max_metric_calls=30)),
    )

    print("Best candidate regex:", result.best_candidate)
    print("Best score:", result.best_score)


if __name__ == "__main__":
    main()
