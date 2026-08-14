from src.database.base import Base
from src.database.session import engine

# These imports register the models with Base.metadata.
from src.database.models.requirement import RequirementRecord
from src.database.models.test_case import TestCaseRecord


def create_tables() -> None:
    Base.metadata.create_all(bind=engine)


if __name__ == "__main__":
    create_tables()
    print("Database tables created successfully.")