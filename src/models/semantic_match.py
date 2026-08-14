from pydantic import BaseModel
## API Response models

class SemanticCandidate(BaseModel):
    test_id: str
    similarity_score: float


class RequirementSemanticMatches(BaseModel):
    requirement_id: str
    requirement_text: str
    candidates: list[SemanticCandidate]