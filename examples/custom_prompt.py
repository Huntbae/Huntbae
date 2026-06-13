"""
Minimal GEPA example with a user-supplied dataset and metric.

Shows the shape of trainset/valset records and how to pass a custom metric.
Use this as a template for your own task: swap in your examples and scoring.

Run:
    python examples/custom_prompt.py
"""

from dotenv import load_dotenv

import gepa

load_dotenv()


trainset = [
    {"input": "Translate to French: 'good morning'", "answer": "bonjour"},
    {"input": "Translate to French: 'thank you'", "answer": "merci"},
    {"input": "Translate to French: 'please'", "answer": "s'il vous plaît"},
]

valset = [
    {"input": "Translate to French: 'hello'", "answer": "bonjour"},
    {"input": "Translate to French: 'goodbye'", "answer": "au revoir"},
]


def metric(example, prediction) -> float:
    gold = example["answer"].strip().lower()
    pred = str(prediction).strip().lower()
    return 1.0 if gold in pred else 0.0


seed_candidate = {
    "system_prompt": "Translate the user's English phrase into French. "
                     "Return only the French translation, no commentary."
}


def main() -> None:
    result = gepa.optimize(
        seed_candidate=seed_candidate,
        trainset=trainset,
        valset=valset,
        task_lm="openai/gpt-4.1-mini",
        reflection_lm="openai/gpt-5",
        max_metric_calls=30,
        metric=metric,
    )

    print("Best prompt:\n", result.best_candidate["system_prompt"])
    print("Best val score:", result.best_val_score)


if __name__ == "__main__":
    main()
