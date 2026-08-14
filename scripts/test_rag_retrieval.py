from src.database.session import SessionLocal
from src.semantic.embedding_service import (
    EmbeddingService,
)
from src.services.rag_retrieval_service import (
    RagRetrievalService,
)


def main() -> None:

    service = RagRetrievalService(
        embedding_service=EmbeddingService()
    )

    session = SessionLocal()

    try:
        documents = service.retrieve(
            session=session,
            question=(
                "What requirements and tests are related "
                "to audit trail recording?"
            ),
        )

        for document in documents:
            print()
            print(
                document.source_type,
                document.source_id,
                document.similarity_score,
            )
            print(document.text)

    finally:
        session.close()


if __name__ == "__main__":
    main()