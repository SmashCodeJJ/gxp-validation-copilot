from sqlalchemy.orm import Session

from src.agent.models import (
    AgentResponse,
    AgentTool,
)
from src.agent.router import AgentRouter
from src.agent.tools import (
    find_semantic_matches_for_requirement,
    get_traceability_for_requirement,
    get_untraced_requirements,
)
from src.services.coverage_analysis_service import (
    CoverageAnalysisService,
)
from src.services.rag_service import RagService


class AgentService:
    def __init__(
        self,
        router: AgentRouter,
        coverage_service: CoverageAnalysisService,
        rag_service: RagService,
    ) -> None:
        self.router = router
        self.coverage_service = coverage_service
        self.rag_service = rag_service

    def answer(
        self,
        session: Session,
        question: str,
    ) -> AgentResponse:
        decision = self.router.route(question)

        if decision.tool == AgentTool.traceability:
            return self._handle_traceability(
                session=session,
                question=question,
                requirement_id=decision.requirement_id,
            )

        if decision.tool == AgentTool.semantic_search:
            return self._handle_semantic_search(
                session=session,
                question=question,
                requirement_id=decision.requirement_id,
            )

        if decision.tool == AgentTool.coverage_analysis:
            return self._handle_coverage_analysis(
                session=session,
                question=question,
                requirement_id=decision.requirement_id,
            )

        return self._handle_rag(
            session=session,
            question=question,
        )

    def _handle_traceability(
        self,
        session: Session,
        question: str,
        requirement_id: str | None,
    ) -> AgentResponse:
        if requirement_id:
            item = get_traceability_for_requirement(
                session=session,
                requirement_id=requirement_id,
            )

            if item is None:
                raise ValueError(
                    f"Requirement not found: {requirement_id}"
                )

            if item["explicitly_traced"]:
                answer = (
                    f"{requirement_id} is explicitly traced "
                    f"to: {', '.join(item['test_ids'])}."
                )
            else:
                answer = (
                    f"{requirement_id} has no explicit "
                    "validation test trace."
                )
        else:
            items = get_untraced_requirements(session)

            if items:
                ids = [
                    item["requirement_id"]
                    for item in items
                ]

                answer = (
                    "Requirements without explicit test "
                    "coverage: "
                    + ", ".join(ids)
                    + "."
                )
            else:
                answer = (
                    "All requirements have explicit test "
                    "coverage."
                )

        return AgentResponse(
            question=question,
            selected_tool=AgentTool.traceability,
            answer=answer,
            requires_human_review=False,
        )

    def _handle_semantic_search(
        self,
        session: Session,
        question: str,
        requirement_id: str | None,
    ) -> AgentResponse:
        if not requirement_id:
            raise ValueError(
                "Semantic search requires a requirement ID."
            )

        matches = find_semantic_matches_for_requirement(
            session=session,
            requirement_id=requirement_id,
        )

        if matches:
            answer = "; ".join(
                f"{item['test_id']} "
                f"(similarity={item['similarity_score']})"
                for item in matches
            )
        else:
            answer = (
                f"No semantic test matches were found for "
                f"{requirement_id}."
            )

        return AgentResponse(
            question=question,
            selected_tool=AgentTool.semantic_search,
            answer=answer,
            requires_human_review=True,
        )

    def _handle_coverage_analysis(
        self,
        session: Session,
        question: str,
        requirement_id: str | None,
    ) -> AgentResponse:
        if not requirement_id:
            raise ValueError(
                "Coverage analysis requires a requirement ID."
            )

        analysis = self.coverage_service.analyze_requirement(
            session=session,
            requirement_id=requirement_id,
            candidate_limit=3,
        )

        if analysis.candidates:
            candidate_summary = "; ".join(
                (
                    f"{candidate.test_id}: "
                    f"{candidate.assessment.coverage.value}"
                )
                for candidate in analysis.candidates
            )
        else:
            candidate_summary = (
                "no candidate tests were found"
            )

        answer = (
            f"Coverage analysis for {requirement_id}: "
            f"{candidate_summary}. "
            f"Review priority: "
            f"{analysis.review_priority.value}."
        )

        return AgentResponse(
            question=question,
            selected_tool=AgentTool.coverage_analysis,
            answer=answer,
            requires_human_review=True,
        )

    def _handle_rag(
        self,
        session: Session,
        question: str,
    ) -> AgentResponse:
        result = self.rag_service.answer_question(
            session=session,
            question=question,
        )

        return AgentResponse(
            question=question,
            selected_tool=AgentTool.rag,
            answer=result.answer,
            requires_human_review=(
                result.requires_human_review
            ),
        )
