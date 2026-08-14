from pathlib import Path

from src.ingestion.protocol_parser import parse_test_cases
from src.ingestion.requirement_parser import (
    extract_requirement_ids,
    read_document,
    parse_requirements
)


def find_missing_requirements(
    urs_path: str,
    protocol_path: str,
) -> list[str]:

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

    all_requirement_ids = {
        requirement.requirement_id
        for requirement in requirements
    }

    covered_requirement_ids = {
        requirement_id
        for test in tests
        for requirement_id in test.related_requirements
    }

    missing = all_requirement_ids - covered_requirement_ids

    return sorted(missing)


if __name__ == "__main__":
    missing = find_missing_requirements(
        "data/synthetic/abfs100/urs.md",
        "data/synthetic/abfs100/validation_tests.md",
    )

    print("Requirements without validation coverage:")

    for requirement in missing:
        print(requirement)