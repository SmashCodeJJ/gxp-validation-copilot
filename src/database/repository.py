from collections import defaultdict

from sqlalchemy import select
from sqlalchemy.orm import Session

from src.database.models.requirement import RequirementRecord
from src.database.models.test_case import TestCaseRecord


def get_all_requirements(
    session: Session,
) -> list[RequirementRecord]:
    statement = (
        select(RequirementRecord)
        .order_by(RequirementRecord.requirement_id)
    )

    return list(session.scalars(statement).all())


def get_all_test_cases(
    session: Session,
) -> list[TestCaseRecord]:
    statement = (
        select(TestCaseRecord)
        .order_by(TestCaseRecord.test_id)
    )

    return list(session.scalars(statement).all())


def build_database_traceability_report(
    session: Session,
) -> list[dict]:
    requirements = get_all_requirements(session)
    test_cases = get_all_test_cases(session)

    tests_by_requirement: dict[str, list[str]] = defaultdict(list)

    for test_case in test_cases:
        for requirement_id in test_case.related_requirements:
            tests_by_requirement[requirement_id].append(
                test_case.test_id
            )

    report = []

    for requirement in requirements:
        test_ids = tests_by_requirement.get(
            requirement.requirement_id,
            [],
        )

        report.append(
            {
                "requirement_id": requirement.requirement_id,
                "requirement_text": requirement.text,
                "explicitly_traced": len(test_ids) > 0,
                "test_ids": test_ids,
            }
        )

    return report

def find_similar_test_cases(
    session: Session,
    requirement_embedding: list[float],
    limit: int = 3,
) -> list[tuple[TestCaseRecord, float]]:
    """
    Find test cases whose embeddings are most similar
    to the supplied requirement embedding.
    """

    distance = TestCaseRecord.embedding.cosine_distance(
        requirement_embedding
    )

    statement = (
        select(
            TestCaseRecord,
            distance.label("distance"),
        )
        .where(
            TestCaseRecord.embedding.is_not(None)
        )
        .order_by(distance)
        .limit(limit)
    )

    rows = session.execute(statement).all()

    return [
        (
            test_case,
            1.0 - float(distance_value),
        )
        for test_case, distance_value in rows
    ]

def find_similar_requirements(
    session: Session,
    query_embedding: list[float],
    limit: int = 5,
) -> list[tuple[RequirementRecord, float]]:

    distance = RequirementRecord.embedding.cosine_distance(
        query_embedding
    )

    statement = (
        select(
            RequirementRecord,
            distance.label("distance"),
        )
        .where(
            RequirementRecord.embedding.is_not(None)
        )
        .order_by(distance)
        .limit(limit)
    )

    rows = session.execute(statement).all()

    return [
        (
            requirement,
            1.0 - float(distance_value),
        )
        for requirement, distance_value in rows
    ]