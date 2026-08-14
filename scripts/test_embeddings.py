from src.semantic.embedding_service import EmbeddingService
from src.semantic.similarity import cosine_similarity


def main() -> None:
    service = EmbeddingService()

    requirement = (
        "The system shall require users to authenticate "
        "before accessing protected functions."
    )

    related_test = (
        "Verify that invalid login credentials prevent "
        "access to protected system functions."
    )

    unrelated_test = (
        "Verify that a bottle with the wrong tablet count "
        "is rejected."
    )

    requirement_embedding = service.embed_text(requirement)
    related_embedding = service.embed_text(related_test)
    unrelated_embedding = service.embed_text(unrelated_test)

    related_score = cosine_similarity(
        requirement_embedding,
        related_embedding,
    )

    unrelated_score = cosine_similarity(
        requirement_embedding,
        unrelated_embedding,
    )

    print(f"Related similarity: {related_score:.3f}")
    print(f"Unrelated similarity: {unrelated_score:.3f}")


if __name__ == "__main__":
    main()