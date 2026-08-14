from src.evaluation.coverage_evaluator import (
    is_dangerous_false_positive,
)


def test_dangerous_false_positive():

    result = is_dangerous_false_positive(
        expected="none",
        predicted="full",
    )

    assert result is True


def test_partial_is_also_dangerous_when_none_expected():

    result = is_dangerous_false_positive(
        expected="none",
        predicted="partial",
    )

    assert result is True


def test_conservative_error_is_not_dangerous():

    result = is_dangerous_false_positive(
        expected="full",
        predicted="partial",
    )

    assert result is False