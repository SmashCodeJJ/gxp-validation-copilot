import pytest

from src.evaluation.rag_evaluator import (
    calculate_citation_precision,
    calculate_source_recall,
    detect_abstention,
)


def test_full_source_recall():

    score = calculate_source_recall(
        expected_source_ids=[
            "URS-008",
            "TEST-005",
        ],
        retrieved_source_ids=[
            "URS-008",
            "TEST-005",
            "TEST-002",
        ],
    )

    assert score == pytest.approx(1.0)


def test_partial_source_recall():

    score = calculate_source_recall(
        expected_source_ids=[
            "URS-008",
            "TEST-005",
        ],
        retrieved_source_ids=[
            "URS-008",
        ],
    )

    assert score == pytest.approx(0.5)


def test_citation_precision():

    score = calculate_citation_precision(
        cited_source_ids=[
            "URS-008",
            "TEST-999",
        ],
        retrieved_source_ids=[
            "URS-008",
            "TEST-005",
        ],
    )

    assert score == pytest.approx(0.5)


def test_detect_abstention():

    answer = (
        "The supplied validation context "
        "does not provide enough information "
        "to determine the answer."
    )

    assert detect_abstention(
        answer
    ) is True