from enum import Enum

from pydantic import BaseModel, Field


class CoverageLevel(str, Enum):
    full = "full"
    partial = "partial"
    none = "none"
    uncertain = "uncertain"


class CoverageAssessment(BaseModel):
    requirement_id: str
    test_id: str

    coverage: CoverageLevel

    confidence: float = Field(
        ge=0.0,
        le=1.0,
    )

    reason: str

    missing_evidence: list[str]

    requires_human_review: bool