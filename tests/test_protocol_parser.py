from pathlib import Path

from src.ingestion.protocol_parser import parse_test_cases
from src.ingestion.requirement_parser import read_document


def test_parse_protocol():
    path = "data/synthetic/abfs100/validation_tests.md"

    text = read_document(path)

    tests = parse_test_cases(
        text=text,
        source_document=Path(path).name,
    )

    assert len(tests) == 6

    assert tests[0].test_id == "TEST-001"

    assert tests[0].related_requirements == ["URS-001"]

    assert tests[3].related_requirements == [
        "URS-005",
        "URS-006",
    ]