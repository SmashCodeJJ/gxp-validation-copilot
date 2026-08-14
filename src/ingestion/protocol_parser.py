import re
from pathlib import Path

from src.ingestion.models import TestCase
from src.ingestion.requirement_parser import read_document


TEST_CASE_PATTERN = re.compile(
    r"##\s*(TEST-\d{3})[^\n]*\n+"
    r"Related Requirements?:\s*(.+?)\n+"
    r"Objective:\s*(.+?)\n+"
    r"Test Steps:\s*(.+?)\n+"
    r"Expected Result:\s*(.+?)"
    r"(?=\n---|\n##\s*TEST-\d{3}|\Z)",
    re.DOTALL,
)


def parse_test_cases(
    text: str,
    source_document: str,
) -> list[TestCase]:
    """Parse validation protocol test cases."""

    matches = TEST_CASE_PATTERN.findall(text)

    print(f"Found {len(matches)} test cases")

    test_cases: list[TestCase] = []

    for (
        test_id,
        related_requirements_text,
        objective,
        test_steps_text,
        expected_result,
    ) in matches:

        related_requirements = re.findall(
            r"URS-\d{3}",
            related_requirements_text,
        )

        test_steps = re.findall(
            r"\d+\.\s*(.+)",
            test_steps_text,
        )

        test_cases.append(
            TestCase(
                test_id=test_id,
                objective=" ".join(objective.split()),
                related_requirements=related_requirements,
                test_steps=[
                    " ".join(step.split())
                    for step in test_steps
                ],
                expected_result=" ".join(
                    expected_result.split()
                ),
                source_document=source_document,
            )
        )

    return test_cases


if __name__ == "__main__":
    path = "data/synthetic/abfs100/validation_tests.md"

    text = read_document(path)

    tests = parse_test_cases(
        text=text,
        source_document=Path(path).name,
    )

    for test_case in tests:
        print(test_case)
        print()