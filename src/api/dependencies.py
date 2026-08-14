from collections.abc import Generator

from sqlalchemy.orm import Session

from src.config.settings import get_settings
from src.database.session import SessionLocal
from src.LLM.coverage_evaluator import CoverageEvaluator
from src.LLM.rag_answerer import RagAnswerer
from src.semantic.embedding_service import EmbeddingService
from src.services.rag_retrieval_service import RagRetrievalService
from src.services.rag_service import RagService


def get_database_session() -> Generator[Session, None, None]:
    session = SessionLocal()

    try:
        yield session
    finally:
        session.close()


def get_embedding_service() -> EmbeddingService:
    settings = get_settings()

    return EmbeddingService(
        model_name=settings.embedding_model
    )


def get_coverage_evaluator() -> CoverageEvaluator:
    settings = get_settings()

    return CoverageEvaluator(
        model_name=settings.openai_model
    )


def get_rag_service() -> RagService:
    settings = get_settings()

    embedding_service = EmbeddingService(
        model_name=settings.embedding_model
    )

    retrieval_service = RagRetrievalService(
        embedding_service=embedding_service
    )

    answerer = RagAnswerer(
        model_name=settings.openai_model
    )

    return RagService(
        retrieval_service=retrieval_service,
        answerer=answerer,
    )