from pydantic import BaseModel


class CoverageEvaluationResult(BaseModel):
    requirement_id: str
    test_id: str

    expected_coverage: str
    predicted_coverage: str

    correct: bool


class CoverageEvaluationSummary(BaseModel):
    total_examples: int
    correct_examples: int

    accuracy: float

    dangerous_false_positives: int
    dangerous_false_positive_rate: float

    results: list[CoverageEvaluationResult]