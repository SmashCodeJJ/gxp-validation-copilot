from sqlalchemy.orm import Session

from src.database.repository import (
    find_similar_requirements,
    find_similar_test_cases,
)
from src.models.retrieval import RetrievedDocument
from src.semantic.embedding_service import EmbeddingService
from src.semantic.text_builder import build_test_embedding_text
from src.ingestion.models import TestCase


class RagRetrievalService:

    def __init__(
        self,
        embedding_service: EmbeddingService,
    ) -> None:
        self.embedding_service = embedding_service

    def retrieve(
        self,
        session: Session,
        question: str,
        requirement_limit: int = 3,
        test_limit: int = 3,
    ) -> list[RetrievedDocument]:

        query_embedding = (
            self.embedding_service.embed_text(question)
        )

        requirement_matches = (
            find_similar_requirements(
                session=session,
                query_embedding=query_embedding,
                limit=requirement_limit,
            )
        )

        test_matches = (
            find_similar_test_cases(
                session=session,
                requirement_embedding=query_embedding,
                limit=test_limit,
            )
        )

        documents: list[RetrievedDocument] = []

        for requirement, score in requirement_matches:
            documents.append(
                RetrievedDocument(
                    source_type="requirement",
                    source_id=requirement.requirement_id,
                    text=requirement.text,
                    source_document=requirement.source_document,
                    similarity_score=round(score, 4),
                )
            )

        for test_case, score in test_matches:

            test_model = TestCase(
                test_id=test_case.test_id,
                objective=test_case.objective,
                related_requirements=(
                    test_case.related_requirements
                ),
                test_steps=test_case.test_steps,
                expected_result=test_case.expected_result,
                source_document=test_case.source_document,
            )

            documents.append(
                RetrievedDocument(
                    source_type="test_case",
                    source_id=test_case.test_id,
                    text=build_test_embedding_text(
                        test_model
                    ),
                    source_document=test_case.source_document,
                    similarity_score=round(score, 4),
                )
            )

        return sorted(
            documents,
            key=lambda document: (
                document.similarity_score
            ),
            reverse=True,
        )