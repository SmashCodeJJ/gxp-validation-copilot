from sqlalchemy import select

from src.database.models.requirement import (
    RequirementRecord,
)
from src.database.repository import (
    find_similar_test_cases,
)
from src.database.session import SessionLocal
from src.evaluation.ground_truth import (
    load_ground_truth,
)
from src.evaluation.retrieval_evaluator import (
    RetrievalEvaluator,
)


GROUND_TRUTH_PATH = (
    "data/evaluation/semantic_ground_truth.csv"
)


def main() -> None:
    session = SessionLocal()

    try:
        ground_truth = load_ground_truth(
            GROUND_TRUTH_PATH
        )

        evaluator = RetrievalEvaluator()

        evaluation_results = []

        for (
            requirement_id,
            expected_test_id,
        ) in ground_truth.items():

            requirement = session.scalar(
                select(RequirementRecord).where(
                    RequirementRecord.requirement_id
                    == requirement_id
                )
            )

            if requirement is None:
                print(
                    f"WARNING: {requirement_id} "
                    f"was not found."
                )
                continue

            if requirement.embedding is None:
                print(
                    f"WARNING: {requirement_id} "
                    f"has no embedding."
                )
                continue

            matches = find_similar_test_cases(
                session=session,
                requirement_embedding=(
                    requirement.embedding
                ),
                limit=3,
            )

            predicted_test_ids = [
                test_case.test_id
                for test_case, _ in matches
            ]

            result = evaluator.evaluate_requirement(
                requirement_id=requirement_id,
                expected_test_id=expected_test_id,
                predicted_test_ids=predicted_test_ids,
            )

            evaluation_results.append(result)

        summary = evaluator.summarize(
            evaluation_results
        )

        print()
        print("=" * 50)
        print("Retrieval Evaluation Report")
        print("=" * 50)

        print(
            f"Requirements evaluated: "
            f"{summary.total_requirements}"
        )

        print(
            f"Top-1 Accuracy: "
            f"{summary.top1_accuracy:.2%}"
        )

        print(
            f"Recall@3: "
            f"{summary.recall_at_3:.2%}"
        )

        print()
        print("Detailed Results")
        print("-" * 50)

        for result in summary.results:

            status = (
                "PASS"
                if result.top1_correct
                else "REVIEW"
            )

            print()
            print(
                f"{result.requirement_id} "
                f"[{status}]"
            )

            print(
                f"Expected: "
                f"{result.expected_test_id}"
            )

            print(
                "Predicted: "
                + ", ".join(
                    result.predicted_test_ids
                )
            )

            print(
                f"Top-1 correct: "
                f"{result.top1_correct}"
            )

            print(
                f"Top-3 correct: "
                f"{result.top3_correct}"
            )

    finally:
        session.close()


if __name__ == "__main__":
    main()