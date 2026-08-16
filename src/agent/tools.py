from sqlalchemy import select
from sqlalchemy.orm import Session

from src.database.models.requirement import RequirementRecord
from src.database.repository import (
    build_database_traceability_report,
    find_similar_test_cases,
)


def get_untraced_requirements(
    session: Session,
) -> list[dict]:

    report = build_database_traceability_report(
        session
    )

    return [
        item
        for item in report
        if not item["explicitly_traced"]
    ]


def get_traceability_for_requirement(
    session: Session,
    requirement_id: str,
) -> dict | None:

    report = build_database_traceability_report(
        session
    )

    for item in report:
        if item["requirement_id"] == requirement_id:
            return item

    return None


def find_semantic_matches_for_requirement(
    session: Session,
    requirement_id: str,
    limit: int = 3,
) -> list[dict]:
    requirement = session.scalar(
        select(RequirementRecord).where(
            RequirementRecord.requirement_id
            == requirement_id
        )
    )

    if requirement is None:
        raise ValueError(
            f"Requirement not found: {requirement_id}"
        )

    if requirement.embedding is None:
        raise ValueError(
            f"Requirement has no embedding: {requirement_id}"
        )

    matches = find_similar_test_cases(
        session=session,
        requirement_embedding=requirement.embedding,
        limit=limit,
    )

    return [
        {
            "test_id": test_case.test_id,
            "similarity_score": round(
                score,
                4,
            ),
        }
        for test_case, score in matches
    ]
