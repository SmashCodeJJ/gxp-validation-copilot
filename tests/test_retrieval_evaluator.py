import pytest

from src.evaluation.retrieval_evaluator import (
    RetrievalEvaluator,
)


def test_top1_and_top3_correct():
    evaluator = RetrievalEvaluator()

    result = evaluator.evaluate_requirement(
        requirement_id="URS-001",
        expected_test_id="TEST-001",
        predicted_test_ids=[
            "TEST-001",
            "TEST-002",
            "TEST-003",
        ],
    )

    assert result.top1_correct is True
    assert result.top3_correct is True


def test_top1_wrong_but_top3_correct():
    evaluator = RetrievalEvaluator()

    result = evaluator.evaluate_requirement(
        requirement_id="URS-001",
        expected_test_id="TEST-001",
        predicted_test_ids=[
            "TEST-002",
            "TEST-001",
            "TEST-003",
        ],
    )

    assert result.top1_correct is False
    assert result.top3_correct is True


def test_top3_wrong():
    evaluator = RetrievalEvaluator()

    result = evaluator.evaluate_requirement(
        requirement_id="URS-001",
        expected_test_id="TEST-001",
        predicted_test_ids=[
            "TEST-002",
            "TEST-003",
            "TEST-004",
        ],
    )

    assert result.top1_correct is False
    assert result.top3_correct is False


def test_summary_metrics():
    evaluator = RetrievalEvaluator()

    results = [
        evaluator.evaluate_requirement(
            "URS-001",
            "TEST-001",
            [
                "TEST-001",
                "TEST-002",
                "TEST-003",
            ],
        ),
        evaluator.evaluate_requirement(
            "URS-002",
            "TEST-002",
            [
                "TEST-001",
                "TEST-002",
                "TEST-003",
            ],
        ),
    ]

    summary = evaluator.summarize(results)

    assert summary.total_requirements == 2

    assert summary.top1_accuracy == pytest.approx(
        0.5
    )

    assert summary.recall_at_3 == pytest.approx(
        1.0
    )