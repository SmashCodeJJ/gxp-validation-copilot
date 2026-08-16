from src.agent.models import (
    AgentDecision,
    AgentTool,
)
from src.evaluation.agent_evaluator import (
    evaluate_routing_case,
    summarize_routing_results,
)


class FakeRouter:
    def __init__(
        self,
        tool: AgentTool,
    ) -> None:
        self.tool = tool

    def route(
        self,
        question: str,
    ) -> AgentDecision:
        return AgentDecision(
            tool=self.tool,
            reason="Unit test.",
        )


def test_evaluate_routing_case_correct():
    result = evaluate_routing_case(
        router=FakeRouter(AgentTool.traceability),
        question=(
            "Which requirements have no explicit "
            "test coverage?"
        ),
        expected_tool="traceability",
    )

    assert result.correct is True
    assert result.predicted_tool == "traceability"


def test_summarize_routing_results():
    results = [
        evaluate_routing_case(
            router=FakeRouter(AgentTool.traceability),
            question="Question one",
            expected_tool="traceability",
        ),
        evaluate_routing_case(
            router=FakeRouter(AgentTool.rag),
            question="Question two",
            expected_tool="semantic_search",
        ),
    ]

    summary = summarize_routing_results(results)

    assert summary.total_examples == 2
    assert summary.correct_examples == 1
    assert summary.accuracy == 0.5
