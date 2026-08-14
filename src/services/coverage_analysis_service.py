from sqlalchemy import select
from sqlalchemy.orm import Session

from src.database.models.requirement import RequirementRecord
from src.database.models.test_case import TestCaseRecord
from src.database.repository import find_similar_test_cases
from src.ingestion.models import Requirement, TestCase
from src.LLM.coverage_evaluator import CoverageEvaluator
from src.models.coverage_analysis import (
    CandidateCoverageResult,
    RequirementCoverageAnalysis,
)
from src.LLM.models import CoverageLevel
from src.models.coverage_analysis import ReviewPriority


def requirement_record_to_model(
    record: RequirementRecord,
) -> Requirement:

    return Requirement(
        requirement_id=record.requirement_id,
        text=record.text,
        source_document=record.source_document,
    )


def test_record_to_model(
    record: TestCaseRecord,
) -> TestCase:

    return TestCase(
        test_id=record.test_id,
        objective=record.objective,
        related_requirements=record.related_requirements,
        test_steps=record.test_steps,
        expected_result=record.expected_result,
        source_document=record.source_document,
    )


class CoverageAnalysisService:

    def __init__(
        self,
        coverage_evaluator: CoverageEvaluator,
    ) -> None:
        self.coverage_evaluator = coverage_evaluator

    def _determine_review_priority(
            self,
            explicit_test_ids: list[str],
            candidate_results: list[CandidateCoverageResult],
    ) -> ReviewPriority:

        if not candidate_results:
            return ReviewPriority.high

        best_assessment = candidate_results[0].assessment

        if not explicit_test_ids:
            return ReviewPriority.high

        if best_assessment.coverage in {
            CoverageLevel.none,
            CoverageLevel.uncertain,
        }:
            return ReviewPriority.high

        if best_assessment.coverage == CoverageLevel.partial:
            return ReviewPriority.medium

        return ReviewPriority.normal

    def _get_explicit_test_ids(
        self,
        session: Session,
        requirement_id: str,
    ) -> list[str]:

        test_cases = session.scalars(
            select(TestCaseRecord)
        ).all()

        return [
            test_case.test_id
            for test_case in test_cases
            if requirement_id
            in test_case.related_requirements
        ]

    def analyze_requirement(
        self,
        session: Session,
        requirement_id: str,
        candidate_limit: int = 3,
    ) -> RequirementCoverageAnalysis:

        requirement_record = session.scalar(
            select(RequirementRecord).where(
                RequirementRecord.requirement_id
                == requirement_id
            )
        )

        if requirement_record is None:
            raise ValueError(
                f"Requirement not found: {requirement_id}"
            )

        if requirement_record.embedding is None:
            raise ValueError(
                f"Requirement has no embedding: {requirement_id}"
            )

        matches = find_similar_test_cases(
            session=session,
            requirement_embedding=(
                requirement_record.embedding
            ),
            limit=candidate_limit,
        )

        requirement = requirement_record_to_model(
            requirement_record
        )

        candidate_results = []

        for test_record, similarity_score in matches:

            test_case = test_record_to_model(
                test_record
            )

            assessment = (
                self.coverage_evaluator.evaluate(
                    requirement=requirement,
                    test_case=test_case,
                )
            )

            candidate_results.append(
                CandidateCoverageResult(
                    test_id=test_record.test_id,
                    similarity_score=round(
                        similarity_score,
                        4,
                    ),
                    assessment=assessment,
                )
            )

        explicit_test_ids = (
            self._get_explicit_test_ids(
                session=session,
                requirement_id=requirement_id,
            )
        )

        review_priority = self._determine_review_priority(
            explicit_test_ids=explicit_test_ids,
            candidate_results=candidate_results,
        )



        return RequirementCoverageAnalysis(
            requirement_id=requirement.requirement_id,
            requirement_text=requirement.text,
            explicitly_traced_test_ids=explicit_test_ids,
            candidates=candidate_results,
            review_priority=review_priority,
            requires_human_review=True,
        )