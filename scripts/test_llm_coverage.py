import os

from dotenv import load_dotenv
from sqlalchemy import select

from src.database.models.requirement import (
    RequirementRecord,
)
from src.database.models.test_case import (
    TestCaseRecord,
)
from src.database.session import SessionLocal
from src.ingestion.models import (
    Requirement,
    TestCase,
)
from src.LLM.coverage_evaluator import (
    CoverageEvaluator,
)


load_dotenv()


def load_requirement(
    session,
    requirement_id: str,
) -> Requirement:

    requirement_record = session.scalar(
        select(RequirementRecord).where(
            RequirementRecord.requirement_id
            == requirement_id
        )
    )

    if requirement_record is None:
        raise RuntimeError(
            f"Requirement not found: {requirement_id}"
        )

    return Requirement(
        requirement_id=(
            requirement_record.requirement_id
        ),
        text=requirement_record.text,
        source_document=(
            requirement_record.source_document
        ),
    )


def load_test_case(
    session,
    test_id: str,
) -> TestCase:

    test_record = session.scalar(
        select(TestCaseRecord).where(
            TestCaseRecord.test_id
            == test_id
        )
    )

    if test_record is None:
        raise RuntimeError(
            f"Test case not found: {test_id}"
        )

    return TestCase(
        test_id=test_record.test_id,
        objective=test_record.objective,
        related_requirements=(
            test_record.related_requirements
        ),
        test_steps=test_record.test_steps,
        expected_result=(
            test_record.expected_result
        ),
        source_document=(
            test_record.source_document
        ),
    )


def run_assessment(
    evaluator: CoverageEvaluator,
    requirement_id: str,
    test_id: str,
) -> None:

    session = SessionLocal()

    try:
        requirement = load_requirement(
            session=session,
            requirement_id=requirement_id,
        )

        test_case = load_test_case(
            session=session,
            test_id=test_id,
        )

        print()
        print("=" * 60)
        print(
            f"Evaluating {requirement_id} "
            f"against {test_id}"
        )
        print("=" * 60)

        print()
        print("Requirement:")
        print(requirement.text)

        print()
        print("Test objective:")
        print(test_case.objective)

        print()
        print("Calling LLM...")

        assessment = evaluator.evaluate(
            requirement=requirement,
            test_case=test_case,
        )

        print()
        print("Coverage Assessment:")
        print(
            assessment.model_dump_json(
                indent=2
            )
        )

    finally:
        session.close()


def main() -> None:

    model_name = os.getenv(
        "OPENAI_MODEL",
        "gpt-5.6",
    )

    evaluator = CoverageEvaluator(
        model_name=model_name
    )

    # Known positive / related pair
    print()
    print("POSITIVE EXAMPLE")

    run_assessment(
        evaluator=evaluator,
        requirement_id="URS-001",
        test_id="TEST-001",
    )

    # Clearly incorrect pair
    print()
    print("NEGATIVE EXAMPLE")

    run_assessment(
        evaluator=evaluator,
        requirement_id="URS-001",
        test_id="TEST-004",
    )


if __name__ == "__main__":
    main()