"""
GEPA Quickstart: optimize a system prompt on the AIME math dataset.

Run:
    python examples/quickstart_aime.py

Requires OPENAI_API_KEY in the environment (or .env file).
"""

from dotenv import load_dotenv

import gepa

load_dotenv()


def main() -> None:
    trainset, valset, _ = gepa.examples.aime.init_dataset()

    seed_candidate = {
        "system_prompt": (
            "You are a helpful assistant. Answer the question. "
            "Put your final answer in the format '### <answer>'."
        )
    }

    result = gepa.optimize(
        seed_candidate=seed_candidate,
        trainset=trainset,
        valset=valset,
        task_lm="openai/gpt-4.1-mini",
        reflection_lm="openai/gpt-5",
        max_metric_calls=150,
    )

    print("=== Best system prompt ===")
    print(result.best_candidate["system_prompt"])
    print("=== Best val score ===")
    print(result.best_val_score)


if __name__ == "__main__":
    main()
