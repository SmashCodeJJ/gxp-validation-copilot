import csv
from pathlib import Path

from sqlalchemy import select
from sqlalchemy.orm import Session

from src.database.models.requirement import RequirementRecord
from src.database.models.test_case import TestCaseRecord
from src.evaluation.coverage_models import (
    CoverageEvaluationResult,
    CoverageEvaluationSummary,
)
from src.ingestion.models import Requirement, TestCase
from src.LLM.coverage_evaluator import CoverageEvaluator


def is_dangerous_false_positive(
    expected: str,
    predicted: str,
) -> bool:
    return (
        expected == "none"
        and predicted in {
            "partial",
            "full",
        }
    )


def requirement_record_to_model(
    record: RequirementRecord,
) -> Requirement:
    return Requirement(
        requirement_id=record.requirement_id,
        text=record.text,
        source_document=record.source_document,
    )


def test_record_to_model(
    record: TestCaseRecord,
) -> TestCase:
    return TestCase(
        test_id=record.test_id,
        objective=record.objective,
        related_requirements=record.related_requirements,
        test_steps=record.test_steps,
        expected_result=record.expected_result,
        source_document=record.source_document,
    )


def evaluate_coverage_model(
    session: Session,
    evaluator: CoverageEvaluator,
    ground_truth_path: str,
) -> CoverageEvaluationSummary:

    results = []

    with open(
        Path(ground_truth_path),
        newline="",
        encoding="utf-8",
    ) as csv_file:

        reader = csv.DictReader(csv_file)

        for row in reader:

            requirement_record = session.scalar(
                select(RequirementRecord).where(
                    RequirementRecord.requirement_id
                    == row["requirement_id"]
                )
            )

            test_record = session.scalar(
                select(TestCaseRecord).where(
                    TestCaseRecord.test_id
                    == row["test_id"]
                )
            )

            if requirement_record is None:
                raise ValueError(
                    f"Missing requirement: "
                    f"{row['requirement_id']}"
                )

            if test_record is None:
                raise ValueError(
                    f"Missing test: "
                    f"{row['test_id']}"
                )

            requirement = requirement_record_to_model(
                requirement_record
            )

            test_case = test_record_to_model(
                test_record
            )

            assessment = evaluator.evaluate(
                requirement=requirement,
                test_case=test_case,
            )

            predicted = assessment.coverage.value
            expected = row["expected_coverage"]

            results.append(
                CoverageEvaluationResult(
                    requirement_id=row["requirement_id"],
                    test_id=row["test_id"],
                    expected_coverage=expected,
                    predicted_coverage=predicted,
                    correct=(predicted == expected),
                )
            )

    total = len(results)

    correct = sum(
        result.correct
        for result in results
    )

    # Part 10 starts here
    dangerous_false_positives = sum(
        is_dangerous_false_positive(
            result.expected_coverage,
            result.predicted_coverage,
        )
        for result in results
    )

    negative_cases = sum(
        result.expected_coverage == "none"
        for result in results
    )

    dangerous_false_positive_rate = (
        dangerous_false_positives
        / negative_cases
        if negative_cases
        else 0.0
    )
    # Part 10 ends here

    return CoverageEvaluationSummary(
        total_examples=total,
        correct_examples=correct,
        accuracy=(
            correct / total
            if total
            else 0.0
        ),
        dangerous_false_positives=(
            dangerous_false_positives
        ),
        dangerous_false_positive_rate=(
            dangerous_false_positive_rate
        ),
        results=results,
    )