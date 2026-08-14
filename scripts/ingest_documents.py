from src.database.ingestion import ingest_validation_package
from src.database.session import SessionLocal
from src.config.settings import get_settings
from src.semantic.embedding_service import EmbeddingService

URS_PATH = "data/synthetic/abfs100/urs.md"
PROTOCOL_PATH = (
    "data/synthetic/abfs100/validation_tests.md"
)


def main() -> None:
    settings = get_settings()

    session = SessionLocal()

    embedding_service = EmbeddingService(
        model_name=settings.embedding_model
    )

    try:
        result = ingest_validation_package(
            session=session,
            urs_path=URS_PATH,
            protocol_path=PROTOCOL_PATH,
            embedding_service=embedding_service,
        )

        print(
            "Validation package ingested successfully."
        )

        print(
            f"Requirements: "
            f"{result['requirements_ingested']}"
        )

        print(
            f"Test cases: "
            f"{result['test_cases_ingested']}"
        )

    except Exception:
        session.rollback()
        raise

    finally:
        session.close()


if __name__ == "__main__":
    main()