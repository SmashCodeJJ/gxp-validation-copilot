from sqlalchemy import select

from src.database.models.requirement import RequirementRecord
from src.database.repository import find_similar_test_cases
from src.database.session import SessionLocal


def main() -> None:
    session = SessionLocal()

    try:
        requirement = session.scalar(
            select(RequirementRecord).where(
                RequirementRecord.requirement_id
                == "URS-001"
            )
        )

        if requirement is None:
            raise RuntimeError(
                "URS-001 was not found."
            )

        if requirement.embedding is None:
            raise RuntimeError(
                "URS-001 does not have an embedding."
            )

        matches = find_similar_test_cases(
            session=session,
            requirement_embedding=requirement.embedding,
            limit=3,
        )

        print()
        print(
            f"Semantic matches for "
            f"{requirement.requirement_id}"
        )

        for test_case, score in matches:
            print(
                f"{test_case.test_id}: "
                f"{score:.4f}"
            )

    finally:
        session.close()


if __name__ == "__main__":
    main()