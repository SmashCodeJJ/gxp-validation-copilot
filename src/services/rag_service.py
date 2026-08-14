import logging
from time import perf_counter

from sqlalchemy.orm import Session

from src.LLM.rag_answerer import RagAnswerer
from src.models.rag import RagAnswer
from src.services.rag_retrieval_service import (
    RagRetrievalService,
)
from src.services.source_validation import (
    validate_rag_sources,
)


logger = logging.getLogger("gxp.rag")


class RagService:
    def __init__(
        self,
        retrieval_service: RagRetrievalService,
        answerer: RagAnswerer,
    ) -> None:
        self.retrieval_service = retrieval_service
        self.answerer = answerer

    def answer_question(
        self,
        session: Session,
        question: str,
    ) -> RagAnswer:

        documents = self.retrieval_service.retrieve(
            session=session,
            question=question,
        )

        if not documents:
            return RagAnswer(
                question=question,
                answer=(
                    "Insufficient validation evidence was "
                    "retrieved to answer this question."
                ),
                sources=[],
                requires_human_review=True,
            )

        answer = self.answerer.answer(
            question=question,
            documents=documents,
        )

        validate_rag_sources(
            answer=answer,
            retrieved_documents=documents,
        )

        return answer