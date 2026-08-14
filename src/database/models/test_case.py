from sqlalchemy import JSON, String, Text
from sqlalchemy.orm import Mapped, mapped_column
from pgvector.sqlalchemy import VECTOR
from src.database.base import Base


class TestCaseRecord(Base):
    __tablename__ = "test_cases"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True,
    )

    test_id: Mapped[str] = mapped_column(
        String(50),
        unique=True,
        nullable=False,
        index=True,
    )

    objective: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    related_requirements: Mapped[list[str]] = mapped_column(
        JSON,
        nullable=False,
    )

    test_steps: Mapped[list[str]] = mapped_column(
        JSON,
        nullable=False,
    )

    expected_result: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    source_document: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    embedding: Mapped[list[float] | None] = mapped_column(
        VECTOR(384),
        nullable=True,
    )