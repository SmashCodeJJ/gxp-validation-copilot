from sqlalchemy import select

from src.database.models.requirement import RequirementRecord
from src.database.repository import find_similar_test_cases
from src.database.session import SessionLocal


def main() -> None:
    session = SessionLocal()

    try:
        requirements = session.scalars(
            select(RequirementRecord).order_by(
                RequirementRecord.requirement_id
            )
        ).all()

        for requirement in requirements:
            if requirement.embedding is None:
                continue

            matches = find_similar_test_cases(
                session=session,
                requirement_embedding=requirement.embedding,
                limit=3,
            )

            print()
            print(
                f"{requirement.requirement_id}: "
                f"{requirement.text}"
            )

            for test_case, score in matches:
                print(
                    f"  {test_case.test_id}: "
                    f"{score:.4f}"
                )

    finally:
        session.close()


if __name__ == "__main__":
    main()