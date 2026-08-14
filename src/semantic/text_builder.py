from src.ingestion.models import Requirement, TestCase


def build_requirement_embedding_text(
    requirement: Requirement,
) -> str:
    return (
        f"User requirement: {requirement.text}"
    )


def build_test_embedding_text(
    test_case: TestCase,
) -> str:

    steps = " ".join(
        f"Step {index}: {step}"
        for index, step in enumerate(
            test_case.test_steps,
            start=1,
        )
    )

    return (
        f"Test objective: {test_case.objective} "
        f"Test procedure: {steps} "
        f"Expected result: {test_case.expected_result}"
    )