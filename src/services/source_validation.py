from src.models.rag import RagAnswer
from src.models.retrieval import RetrievedDocument


def validate_rag_sources(
    answer: RagAnswer,
    retrieved_documents: list[RetrievedDocument],
) -> None:

    allowed_sources = {
        (
            document.source_type,
            document.source_id,
            document.source_document,
        )
        for document in retrieved_documents
    }

    for source in answer.sources:

        source_key = (
            source.source_type,
            source.source_id,
            source.source_document,
        )

        if source_key not in allowed_sources:
            raise ValueError(
                f"LLM returned unsupported source: "
                f"{source.source_id}"
            )