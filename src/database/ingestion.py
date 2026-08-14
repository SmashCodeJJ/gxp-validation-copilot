from pathlib import Path

from sqlalchemy.orm import Session

from src.database.models.requirement import RequirementRecord
from src.database.models.test_case import TestCaseRecord
from src.ingestion.protocol_parser import parse_test_cases
from src.ingestion.requirement_parser import (
    parse_requirements,
    read_document,
)
from src.semantic.embedding_service import EmbeddingService
from src.semantic.text_builder import (
    build_requirement_embedding_text,
    build_test_embedding_text,
)


def ingest_requirements(
    session: Session,
    urs_path: str,
    embedding_service: EmbeddingService,
) -> int:

    text = read_document(urs_path)

    requirements = parse_requirements(
        text=text,
        source_document=Path(urs_path).name,
    )

    embedding_texts = [
        build_requirement_embedding_text(requirement)
        for requirement in requirements
    ]

    embeddings = embedding_service.embed_texts(
        embedding_texts
    )

    for requirement, embedding in zip(
        requirements,
        embeddings,
    ):
        existing_record = (
            session.query(RequirementRecord)
            .filter(
                RequirementRecord.requirement_id
                == requirement.requirement_id
            )
            .one_or_none()
        )

        if existing_record:
            existing_record.text = requirement.text
            existing_record.source_document = (
                requirement.source_document
            )
            existing_record.embedding = embedding

        else:
            session.add(
                RequirementRecord(
                    requirement_id=requirement.requirement_id,
                    text=requirement.text,
                    source_document=requirement.source_document,
                    embedding=embedding,
                )
            )

    session.commit()

    return len(requirements)

def ingest_test_cases(
    session: Session,
    protocol_path: str,
    embedding_service: EmbeddingService,
) -> int:

    text = read_document(protocol_path)

    test_cases = parse_test_cases(
        text=text,
        source_document=Path(protocol_path).name,
    )

    embedding_texts = [
        build_test_embedding_text(test_case)
        for test_case in test_cases
    ]

    embeddings = embedding_service.embed_texts(
        embedding_texts
    )

    for test_case, embedding in zip(
        test_cases,
        embeddings,
    ):
        existing_record = (
            session.query(TestCaseRecord)
            .filter(
                TestCaseRecord.test_id
                == test_case.test_id
            )
            .one_or_none()
        )

        if existing_record:
            existing_record.objective = (
                test_case.objective
            )

            existing_record.related_requirements = (
                test_case.related_requirements
            )

            existing_record.test_steps = (
                test_case.test_steps
            )

            existing_record.expected_result = (
                test_case.expected_result
            )

            existing_record.source_document = (
                test_case.source_document
            )

            existing_record.embedding = embedding

        else:
            session.add(
                TestCaseRecord(
                    test_id=test_case.test_id,
                    objective=test_case.objective,
                    related_requirements=(
                        test_case.related_requirements
                    ),
                    test_steps=test_case.test_steps,
                    expected_result=(
                        test_case.expected_result
                    ),
                    source_document=(
                        test_case.source_document
                    ),
                    embedding=embedding,
                )
            )

    session.commit()

    return len(test_cases)

def ingest_validation_package(
    session: Session,
    urs_path: str,
    protocol_path: str,
    embedding_service: EmbeddingService,
) -> dict[str, int]:

    requirement_count = ingest_requirements(
        session=session,
        urs_path=urs_path,
        embedding_service=embedding_service,
    )

    test_case_count = ingest_test_cases(
        session=session,
        protocol_path=protocol_path,
        embedding_service=embedding_service,
    )

    return {
        "requirements_ingested": requirement_count,
        "test_cases_ingested": test_case_count,
    }