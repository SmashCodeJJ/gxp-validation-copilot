from src.agent.router import AgentRouter
from src.config.settings import get_settings
from src.evaluation.agent_evaluator import (
    evaluate_agent_router,
)


GROUND_TRUTH_PATH = (
    "data/evaluation/agent_routing.csv"
)


def main() -> None:
    settings = get_settings()

    router = AgentRouter(
        model_name=settings.openai_model
    )

    summary = evaluate_agent_router(
        router=router,
        ground_truth_path=GROUND_TRUTH_PATH,
    )

    print()
    print("=" * 50)
    print("Agent Routing Evaluation")
    print("=" * 50)

    print(
        f"Examples: {summary.total_examples}"
    )
    print(
        f"Accuracy: {summary.accuracy:.2%}"
    )

    for result in summary.results:
        status = (
            "PASS"
            if result.correct
            else "FAIL"
        )

        print()
        print(f"{status}: {result.question}")
        print(
            f"  Expected: {result.expected_tool}"
        )
        print(
            f"  Predicted: {result.predicted_tool}"
        )


if __name__ == "__main__":
    main()
