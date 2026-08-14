from pathlib import Path

from src.ingestion.protocol_parser import parse_test_cases
from src.ingestion.requirement_parser import (
    parse_requirements,
    read_document,
)
from src.semantic.embedding_service import EmbeddingService
from src.semantic.matcher import SemanticMatcher


URS_PATH = "data/synthetic/abfs100/urs.md"
PROTOCOL_PATH = (
    "data/synthetic/abfs100/validation_tests.md"
)


def main() -> None:
    requirements = parse_requirements(
        text=read_document(URS_PATH),
        source_document=Path(URS_PATH).name,
    )

    test_cases = parse_test_cases(
        text=read_document(PROTOCOL_PATH),
        source_document=Path(PROTOCOL_PATH).name,
    )

    embedding_service = EmbeddingService()
    matcher = SemanticMatcher(embedding_service)

    for requirement in requirements:
        matches = matcher.rank_tests_for_requirement(
            requirement=requirement,
            test_cases=test_cases,
        )

        print()
        print(
            f"{requirement.requirement_id}: "
            f"{requirement.text}"
        )

        for match in matches[:3]:
            print(
                f"  {match.test_id}: "
                f"{match.similarity_score:.4f}"
            )


if __name__ == "__main__":
    main()