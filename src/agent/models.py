from enum import Enum

from pydantic import BaseModel, Field


class AgentTool(str, Enum):
    traceability = "traceability"
    semantic_search = "semantic_search"
    coverage_analysis = "coverage_analysis"
    rag = "rag"


class AgentDecision(BaseModel):
    tool: AgentTool

    requirement_id: str | None = None
    test_id: str | None = None

    reason: str


class AgentRequest(BaseModel):
    question: str = Field(
        min_length=3,
        max_length=1000,
    )


class AgentResponse(BaseModel):
    question: str
    selected_tool: AgentTool
    answer: str
    requires_human_review: bool
