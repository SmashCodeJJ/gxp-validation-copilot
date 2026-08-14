from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from src.api.dependencies import (
    get_coverage_evaluator,
    get_database_session,
)
from src.database.models.requirement import RequirementRecord
from src.database.repository import (
    build_database_traceability_report,
    find_similar_test_cases,
    get_all_requirements,
    get_all_test_cases,
)
from src.ingestion.models import Requirement, TestCase
from src.LLM.coverage_evaluator import CoverageEvaluator
from src.models.coverage_analysis import (
    RequirementCoverageAnalysis,
)
from src.models.semantic_match import (
    RequirementSemanticMatches,
    SemanticCandidate,
)
from src.models.traceability import TraceabilityItem
from src.services.coverage_analysis_service import (
    CoverageAnalysisService,
)


router = APIRouter(
    tags=["Validation"],
)


DatabaseSession = Annotated[
    Session,
    Depends(get_database_session),
]


CoverageEvaluatorDependency = Annotated[
    CoverageEvaluator,
    Depends(get_coverage_evaluator),
]


@router.get(
    "/requirements",
    response_model=list[Requirement],
)
def get_requirements_endpoint(
    session: DatabaseSession,
):
    records = get_all_requirements(session)

    return [
        Requirement(
            requirement_id=record.requirement_id,
            text=record.text,
            source_document=record.source_document,
        )
        for record in records
    ]


@router.get(
    "/tests",
    response_model=list[TestCase],
)
def get_tests_endpoint(
    session: DatabaseSession,
):
    records = get_all_test_cases(session)

    return [
        TestCase(
            test_id=record.test_id,
            objective=record.objective,
            related_requirements=record.related_requirements,
            test_steps=record.test_steps,
            expected_result=record.expected_result,
            source_document=record.source_document,
        )
        for record in records
    ]


@router.get(
    "/traceability",
    response_model=list[TraceabilityItem],
)
def get_traceability(
    session: DatabaseSession,
):
    return build_database_traceability_report(
        session
    )


@router.get(
    "/requirements/{requirement_id}/semantic-matches",
    response_model=RequirementSemanticMatches,
)
def get_semantic_matches(
    requirement_id: str,
    session: DatabaseSession,
):
    requirement = session.scalar(
        select(RequirementRecord).where(
            RequirementRecord.requirement_id
            == requirement_id
        )
    )

    if requirement is None:
        raise HTTPException(
            status_code=404,
            detail="Requirement not found.",
        )

    if requirement.embedding is None:
        raise HTTPException(
            status_code=409,
            detail=(
                "Requirement embedding is unavailable."
            ),
        )

    matches = find_similar_test_cases(
        session=session,
        requirement_embedding=requirement.embedding,
        limit=3,
    )

    return RequirementSemanticMatches(
        requirement_id=requirement.requirement_id,
        requirement_text=requirement.text,
        candidates=[
            SemanticCandidate(
                test_id=test_case.test_id,
                similarity_score=round(
                    score,
                    4,
                ),
            )
            for test_case, score in matches
        ],
    )


@router.get(
    "/requirements/{requirement_id}/coverage-analysis",
    response_model=RequirementCoverageAnalysis,
)
def get_coverage_analysis(
    requirement_id: str,
    session: DatabaseSession,
    evaluator: CoverageEvaluatorDependency,
):
    service = CoverageAnalysisService(
        coverage_evaluator=evaluator
    )

    try:
        return service.analyze_requirement(
            session=session,
            requirement_id=requirement_id,
            candidate_limit=3,
        )

    except ValueError as error:
        raise HTTPException(
            status_code=404,
            detail=str(error),
        ) from error