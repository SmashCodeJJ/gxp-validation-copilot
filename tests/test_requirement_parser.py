from pathlib import Path

from src.ingestion.requirement_parser import (
    parse_requirements,
    read_document,
)


def test_parse_requirements():
    path = "data/synthetic/abfs100/urs.md"

    text = read_document(path)

    requirements = parse_requirements(
        text=text,
        source_document=Path(path).name,
    )

    assert len(requirements) == 12

    assert requirements[0].requirement_id == "URS-001"

    assert requirements[-1].requirement_id == "URS-012"

    assert "authenticate" in requirements[0].text.lower()