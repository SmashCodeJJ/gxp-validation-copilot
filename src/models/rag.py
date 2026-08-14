from pydantic import BaseModel


class SourceReference(BaseModel):
    source_type: str
    source_id: str
    source_document: str


class RagAnswer(BaseModel):
    question: str
    answer: str
    sources: list[SourceReference]
    requires_human_review: bool