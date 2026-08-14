from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column
from pgvector.sqlalchemy import VECTOR

from src.database.base import Base


class RequirementRecord(Base):
    __tablename__ = "requirements"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True,
    )

    requirement_id: Mapped[str] = mapped_column(
        String(50),
        unique=True,
        nullable=False,
        index=True,
    )

    text: Mapped[str] = mapped_column(
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