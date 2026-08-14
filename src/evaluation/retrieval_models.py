from pydantic import BaseModel


class RetrievalEvaluationResult(BaseModel):
    requirement_id: str
    expected_test_id: str
    predicted_test_ids: list[str]

    top1_correct: bool
    top3_correct: bool


class RetrievalEvaluationSummary(BaseModel):
    total_requirements: int

    top1_accuracy: float
    recall_at_3: float

    results: list[RetrievalEvaluationResult]