from pydantic import BaseModel, Field


class RagQuestion(BaseModel):
    question: str = Field(
        min_length=3,
        max_length=1000,
    )