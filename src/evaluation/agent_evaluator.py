import csv
from pathlib import Path

from pydantic import BaseModel

from src.agent.router import AgentRouter


class RoutingEvaluationResult(BaseModel):
    question: str
    expected_tool: str
    predicted_tool: str
    correct: bool


class RoutingEvaluationSummary(BaseModel):
    total_examples: int
    correct_examples: int
    accuracy: float
    results: list[RoutingEvaluationResult]


def evaluate_routing_case(
    router: AgentRouter,
    question: str,
    expected_tool: str,
) -> RoutingEvaluationResult:
    decision = router.route(question)

    predicted_tool = decision.tool.value

    return RoutingEvaluationResult(
        question=question,
        expected_tool=expected_tool,
        predicted_tool=predicted_tool,
        correct=predicted_tool == expected_tool,
    )


def summarize_routing_results(
    results: list[RoutingEvaluationResult],
) -> RoutingEvaluationSummary:
    total_examples = len(results)
    correct_examples = sum(
        result.correct
        for result in results
    )

    return RoutingEvaluationSummary(
        total_examples=total_examples,
        correct_examples=correct_examples,
        accuracy=(
            correct_examples / total_examples
            if total_examples
            else 0.0
        ),
        results=results,
    )


def evaluate_agent_router(
    router: AgentRouter,
    ground_truth_path: str,
) -> RoutingEvaluationSummary:
    results = []

    with Path(ground_truth_path).open(
        newline="",
        encoding="utf-8",
    ) as csv_file:
        reader = csv.DictReader(csv_file)

        for row in reader:
            results.append(
                evaluate_routing_case(
                    router=router,
                    question=row["question"],
                    expected_tool=row["expected_tool"],
                )
            )

    return summarize_routing_results(results)
