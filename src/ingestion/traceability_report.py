from pathlib import Path

from src.ingestion.protocol_parser import parse_test_cases
from src.ingestion.requirement_parser import (
    parse_requirements,
    read_document,
)


def build_traceability_report(
    urs_path: str,
    protocol_path: str,
) -> list[dict]:
    urs_text = read_document(urs_path)
    protocol_text = read_document(protocol_path)

    requirements = parse_requirements(
        text=urs_text,
        source_document=Path(urs_path).name,
    )

    tests = parse_test_cases(
        text=protocol_text,
        source_document=Path(protocol_path).name,
    )

    tests_by_requirement: dict[str, list] = {}

    for test in tests:
        for requirement_id in test.related_requirements:
            tests_by_requirement.setdefault(
                requirement_id,
                [],
            ).append(test)

    report = []

    for requirement in requirements:
        related_tests = tests_by_requirement.get(
            requirement.requirement_id,
            [],
        )

        report.append(
            {
                "requirement_id": requirement.requirement_id,
                "requirement_text": requirement.text,
                "explicitly_traced": len(related_tests) > 0,
                "test_ids": [
                    test.test_id
                    for test in related_tests
                ],
            }
        )

    return report