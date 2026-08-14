from collections.abc import Generator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

from src.api.dependencies import get_database_session
from src.api.main import app
from src.database.base import Base
from src.database.models.requirement import RequirementRecord
from src.database.models.test_case import TestCaseRecord


TEST_DATABASE_URL = "sqlite+pysqlite:///:memory:"


test_engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={
        "check_same_thread": False,
    },
    poolclass=StaticPool,
)


TestingSessionLocal = sessionmaker(
    bind=test_engine,
    autoflush=False,
    expire_on_commit=False,
)


@pytest.fixture
def database_session() -> Generator[Session, None, None]:
    Base.metadata.create_all(bind=test_engine)

    session = TestingSessionLocal()

    try:
        seed_test_database(session)
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind=test_engine)


def seed_test_database(
    session: Session,
) -> None:
    requirements = [
        RequirementRecord(
            requirement_id="URS-001",
            text="Users shall authenticate before access.",
            source_document="urs.md",
        ),
        RequirementRecord(
            requirement_id="URS-002",
            text="Operator access shall be role restricted.",
            source_document="urs.md",
        ),
        RequirementRecord(
            requirement_id="URS-003",
            text="Only approved recipes shall be selectable.",
            source_document="urs.md",
        ),
    ]

    test_cases = [
        TestCaseRecord(
            test_id="TEST-001",
            objective="Verify invalid login is rejected.",
            related_requirements=["URS-001"],
            test_steps=[
                "Open login page.",
                "Enter invalid credentials.",
            ],
            expected_result="Access is denied.",
            source_document="validation_tests.md",
        ),
        TestCaseRecord(
            test_id="TEST-002",
            objective="Verify role-based access.",
            related_requirements=["URS-002"],
            test_steps=[
                "Log in as Operator.",
                "Attempt administrator function.",
            ],
            expected_result="Access is denied.",
            source_document="validation_tests.md",
        ),
    ]

    session.add_all(requirements)
    session.add_all(test_cases)
    session.commit()


@pytest.fixture
def client(
    database_session: Session,
) -> Generator[TestClient, None, None]:

    def override_database_session():
        yield database_session

    app.dependency_overrides[
        get_database_session
    ] = override_database_session

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()