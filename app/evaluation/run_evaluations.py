import json

from app.pipeline import RagPipeline
from app.evaluation.evaluator import (
    hit_rate,
    mean_reciprocal_rank
)


def main():
    print("Initializing RAG pipeline...")
    pipeline = RagPipeline()

    print("Loading test set...")
    with open(
        "app/evaluation/test_set.json",
        "r",
        encoding="utf-8"
    ) as f:
        test_set = json.load(f)

    print("Running evaluation...")

    hr, misses = hit_rate(pipeline, test_set)
    mrr = mean_reciprocal_rank(pipeline, test_set)

    print("\n" + "=" * 40)
    print("RAG EVALUATION RESULTS")
    print("=" * 40)
    print(f"Questions Tested : {len(test_set)}")
    print(f"Hit Rate         : {hr:.2%}")
    print(f"MRR              : {mrr:.4f}")
    print("=" * 40)
    if misses:
        print("\nMISSED QUESTIONS:")
        for m in misses:
            print(f"  - {m['question']} (expected page {m['expected_page']})")

if __name__ == "__main__":
    main()