from collections.abc import Generator

from fastapi.testclient import TestClient

from src.agent.models import (
    AgentResponse,
    AgentTool,
)
from src.api.dependencies import get_agent_service
from src.api.main import app


class FakeAgentService:
    def answer(
        self,
        session,
        question: str,
    ) -> AgentResponse:
        return AgentResponse(
            question=question,
            selected_tool=AgentTool.traceability,
            answer=(
                "Requirements without explicit test "
                "coverage: URS-003."
            ),
            requires_human_review=False,
        )


def test_agent_query_endpoint(
    client: TestClient,
):
    def override_agent_service() -> Generator[
        FakeAgentService,
        None,
        None,
    ]:
        yield FakeAgentService()

    app.dependency_overrides[
        get_agent_service
    ] = override_agent_service

    try:
        response = client.post(
            "/api/v1/agent/query",
            json={
                "question": (
                    "Which requirements have no explicit "
                    "test coverage?"
                )
            },
        )
    finally:
        app.dependency_overrides.pop(
            get_agent_service,
            None,
        )

    assert response.status_code == 200
    assert response.json() == {
        "question": (
            "Which requirements have no explicit "
            "test coverage?"
        ),
        "selected_tool": "traceability",
        "answer": (
            "Requirements without explicit test "
            "coverage: URS-003."
        ),
        "requires_human_review": False,
    }
