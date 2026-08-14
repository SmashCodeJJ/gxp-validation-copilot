from pydantic import BaseModel

from src.ingestion.models import Requirement, TestCase
from src.semantic.embedding_service import EmbeddingService
from src.semantic.similarity import cosine_similarity
from src.semantic.text_builder import build_test_embedding_text


class SemanticMatch(BaseModel):
    requirement_id: str
    test_id: str
    similarity_score: float


class SemanticMatcher:
    def __init__(
        self,
        embedding_service: EmbeddingService,
    ) -> None:
        self.embedding_service = embedding_service

    def rank_tests_for_requirement(
        self,
        requirement: Requirement,
        test_cases: list[TestCase],
    ) -> list[SemanticMatch]:
        requirement_embedding = (
            self.embedding_service.embed_text(
                requirement.text
            )
        )

        test_texts = [
            build_test_embedding_text(test_case)
            for test_case in test_cases
        ]

        test_embeddings = (
            self.embedding_service.embed_texts(test_texts)
        )

        matches = []

        for test_case, test_embedding in zip(
            test_cases,
            test_embeddings,
        ):
            score = cosine_similarity(
                requirement_embedding,
                test_embedding,
            )

            matches.append(
                SemanticMatch(
                    requirement_id=(
                        requirement.requirement_id
                    ),
                    test_id=test_case.test_id,
                    similarity_score=round(score, 4),
                )
            )

        return sorted(
            matches,
            key=lambda match: match.similarity_score,
            reverse=True,
        )