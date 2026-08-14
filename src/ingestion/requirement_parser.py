import re
from pathlib import Path

from src.ingestion.models import Requirement


REQUIREMENT_PATTERN = re.compile(
    r"^#{1,6}\s+(URS-\d{3})[^\n]*\n+"
    r"(.+?)"
    r"(?=^#{1,6}\s+URS-\d{3}|\Z)",
    re.MULTILINE | re.DOTALL,
)


def read_document(path: str) -> str:
    """Read a UTF-8 text document."""
    file_path = Path(path)

    if not file_path.exists():
        raise FileNotFoundError(f"Document not found: {path}")

    return file_path.read_text(encoding="utf-8")


def extract_requirement_ids(text: str) -> list[str]:
    """Extract unique URS requirement IDs."""
    return sorted(set(re.findall(r"URS-\d{3}", text)))


def parse_requirements(
    text: str,
    source_document: str,
) -> list[Requirement]:
    """
    Parse URS requirements into structured Requirement objects.
    """

    matches = REQUIREMENT_PATTERN.findall(text)

    requirements: list[Requirement] = []

    for requirement_id, requirement_text in matches:
        cleaned_text = " ".join(requirement_text.split())

        requirements.append(
            Requirement(
                requirement_id=requirement_id,
                text=cleaned_text,
                source_document=source_document,
            )
        )

    return requirements


if __name__ == "__main__":
    path = "data/synthetic/abfs100/urs.md"

    text = read_document(path)

    requirements = parse_requirements(
        text=text,
        source_document=Path(path).name,
    )

    for requirement in requirements:
        print(requirement)