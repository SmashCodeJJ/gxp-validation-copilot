from pydantic import BaseModel


class RagEvaluationCase(BaseModel):
    question: str
    expected_source_ids: list[str]
    answerable: bool


class RagEvaluationResult(BaseModel):
    question: str

    expected_source_ids: list[str]
    retrieved_source_ids: list[str]
    cited_source_ids: list[str]

    answerable: bool

    source_recall: float
    citation_precision: float

    abstention_correct: bool | None

    answer: str


class RagEvaluationSummary(BaseModel):
    total_questions: int

    average_source_recall: float
    average_citation_precision: float

    answerable_questions: int
    unanswerable_questions: int

    correct_abstentions: int
    abstention_accuracy: float

    results: list[RagEvaluationResult]