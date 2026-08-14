import os

from dotenv import load_dotenv

from src.database.session import SessionLocal
from src.evaluation.coverage_evaluator import (
    evaluate_coverage_model,
)
from src.LLM.coverage_evaluator import CoverageEvaluator


load_dotenv()


GROUND_TRUTH_PATH = (
    "data/evaluation/coverage_ground_truth.csv"
)


def main() -> None:

    model_name = os.getenv(
        "OPENAI_MODEL",
        "gpt-5-mini",
    )

    evaluator = CoverageEvaluator(
        model_name=model_name
    )

    session = SessionLocal()

    try:
        summary = evaluate_coverage_model(
            session=session,
            evaluator=evaluator,
            ground_truth_path=GROUND_TRUTH_PATH,
        )

        print()
        print("=" * 50)
        print("LLM Coverage Evaluation")
        print("=" * 50)

        print(
            f"Examples: "
            f"{summary.total_examples}"
        )

        print(
            f"Accuracy: "
            f"{summary.accuracy:.2%}"
        )

        print()

        for result in summary.results:

            status = (
                "PASS"
                if result.correct
                else "FAIL"
            )

            print(
                f"{result.requirement_id} "
                f"+ {result.test_id}: "
                f"{status}"
            )

            print(
                f"  Expected: "
                f"{result.expected_coverage}"
            )

            print(
                f"  Predicted: "
                f"{result.predicted_coverage}"
            )

    finally:
        session.close()


if __name__ == "__main__":
    main()