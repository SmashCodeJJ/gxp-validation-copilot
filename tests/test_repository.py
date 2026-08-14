from sqlalchemy.orm import Session

from src.database.repository import (
    build_database_traceability_report,
    get_all_requirements,
    get_all_test_cases,
)


def test_get_all_requirements(
    database_session: Session,
):
    requirements = get_all_requirements(
        database_session
    )

    assert len(requirements) == 3
    assert requirements[0].requirement_id == "URS-001"


def test_get_all_test_cases(
    database_session: Session,
):
    tests = get_all_test_cases(
        database_session
    )

    assert len(tests) == 2
    assert tests[0].test_id == "TEST-001"


def test_build_database_traceability_report(
    database_session: Session,
):
    report = build_database_traceability_report(
        database_session
    )

    assert len(report) == 3

    report_by_requirement = {
        item["requirement_id"]: item
        for item in report
    }

    assert report_by_requirement["URS-001"][
        "test_ids"
    ] == ["TEST-001"]

    assert report_by_requirement["URS-003"][
        "explicitly_traced"
    ] is False