from enum import Enum

from pydantic import BaseModel

from src.LLM.models import CoverageAssessment


class ReviewPriority(str, Enum):
    normal = "normal"
    medium = "medium"
    high = "high"


class CandidateCoverageResult(BaseModel):
    test_id: str
    similarity_score: float
    assessment: CoverageAssessment


class RequirementCoverageAnalysis(BaseModel):
    requirement_id: str
    requirement_text: str

    explicitly_traced_test_ids: list[str]

    candidates: list[CandidateCoverageResult]

    review_priority: ReviewPriority
    requires_human_review: bool