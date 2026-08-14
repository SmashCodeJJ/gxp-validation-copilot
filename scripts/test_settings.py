from src.config.settings import (
    get_settings,
)


def main() -> None:

    settings = get_settings()

    print(
        "Environment:",
        settings.environment,
    )

    print(
        "Database:",
        settings.database_url,
    )

    print(
        "OpenAI model:",
        settings.openai_model,
    )

    print(
        "Embedding model:",
        settings.embedding_model,
    )

    print(
        "Semantic Top-K:",
        settings.semantic_top_k,
    )


if __name__ == "__main__":
    main()