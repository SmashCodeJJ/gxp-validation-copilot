import pytest
from sqlalchemy.orm import Session

from src.LLM.models import (
    CoverageAssessment,
    CoverageLevel,
)
from src.agent.models import (
    AgentDecision,
    AgentTool,
)
from src.agent.service import AgentService
from src.models.coverage_analysis import (
    CandidateCoverageResult,
    RequirementCoverageAnalysis,
    ReviewPriority,
)
from src.models.rag import RagAnswer


class FakeRouter:
    def __init__(
        self,
        decision: AgentDecision,
    ) -> None:
        self.decision = decision

    def route(
        self,
        question: str,
    ) -> AgentDecision:
        return self.decision


class FakeCoverageService:
    def analyze_requirement(
        self,
        session: Session,
        requirement_id: str,
        candidate_limit: int = 3,
    ) -> RequirementCoverageAnalysis:
        return RequirementCoverageAnalysis(
            requirement_id=requirement_id,
            requirement_text=(
                "Users shall authenticate before access."
            ),
            explicitly_traced_test_ids=["TEST-001"],
            candidates=[
                CandidateCoverageResult(
                    test_id="TEST-001",
                    similarity_score=0.91,
                    assessment=CoverageAssessment(
                        requirement_id=requirement_id,
                        test_id="TEST-001",
                        coverage=CoverageLevel.full,
                        confidence=0.9,
                        reason="Evidence is sufficient.",
                        missing_evidence=[],
                        requires_human_review=True,
                    ),
                )
            ],
            review_priority=ReviewPriority.normal,
            requires_human_review=True,
        )


class FakeRagService:
    def answer_question(
        self,
        session: Session,
        question: str,
    ) -> RagAnswer:
        return RagAnswer(
            question=question,
            answer="Audit trail evidence is described in URS-008.",
            sources=[],
            requires_human_review=True,
        )


def build_service(
    decision: AgentDecision,
) -> AgentService:
    return AgentService(
        router=FakeRouter(decision),
        coverage_service=FakeCoverageService(),
        rag_service=FakeRagService(),
    )


def test_agent_routes_to_untraced_requirements(
    database_session: Session,
):
    service = build_service(
        AgentDecision(
            tool=AgentTool.traceability,
            reason="Unit test.",
        )
    )

    response = service.answer(
        session=database_session,
        question=(
            "Which requirements have no explicit "
            "test coverage?"
        ),
    )

    assert response.selected_tool == AgentTool.traceability
    assert "URS-003" in response.answer
    assert response.requires_human_review is False


def test_agent_routes_to_requirement_traceability(
    database_session: Session,
):
    service = build_service(
        AgentDecision(
            tool=AgentTool.traceability,
            requirement_id="URS-001",
            reason="Unit test.",
        )
    )

    response = service.answer(
        session=database_session,
        question="Is URS-001 explicitly traced?",
    )

    assert response.selected_tool == AgentTool.traceability
    assert "TEST-001" in response.answer


def test_agent_routes_to_semantic_search(
    database_session: Session,
    monkeypatch: pytest.MonkeyPatch,
):
    def fake_semantic_matches(
        session: Session,
        requirement_id: str,
    ) -> list[dict]:
        return [
            {
                "test_id": "TEST-002",
                "similarity_score": 0.72,
            }
        ]

    monkeypatch.setattr(
        "src.agent.service.find_semantic_matches_for_requirement",
        fake_semantic_matches,
    )

    service = build_service(
        AgentDecision(
            tool=AgentTool.semantic_search,
            requirement_id="URS-003",
            reason="Unit test.",
        )
    )

    response = service.answer(
        session=database_session,
        question="Show similar tests for URS-003.",
    )

    assert response.selected_tool == AgentTool.semantic_search
    assert "TEST-002" in response.answer
    assert response.requires_human_review is True


def test_agent_routes_to_coverage_analysis(
    database_session: Session,
):
    service = build_service(
        AgentDecision(
            tool=AgentTool.coverage_analysis,
            requirement_id="URS-001",
            reason="Unit test.",
        )
    )

    response = service.answer(
        session=database_session,
        question="Does URS-001 have adequate coverage?",
    )

    assert response.selected_tool == AgentTool.coverage_analysis
    assert "TEST-001: full" in response.answer
    assert "Review priority: normal" in response.answer
    assert response.requires_human_review is True


def test_agent_routes_to_rag(
    database_session: Session,
):
    service = build_service(
        AgentDecision(
            tool=AgentTool.rag,
            reason="Unit test.",
        )
    )

    response = service.answer(
        session=database_session,
        question="Explain audit trail validation evidence.",
    )

    assert response.selected_tool == AgentTool.rag
    assert "URS-008" in response.answer
    assert response.requires_human_review is True


def test_semantic_search_requires_requirement_id(
    database_session: Session,
):
    service = build_service(
        AgentDecision(
            tool=AgentTool.semantic_search,
            reason="Unit test.",
        )
    )

    with pytest.raises(
        ValueError,
        match="requires a requirement ID",
    ):
        service.answer(
            session=database_session,
            question="Show similar tests.",
        )
