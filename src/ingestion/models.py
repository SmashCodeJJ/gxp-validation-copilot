from pydantic import BaseModel


class Requirement(BaseModel):
    requirement_id: str
    text: str
    source_document: str


class TestCase(BaseModel):
    test_id: str
    objective: str
    related_requirements: list[str]
    test_steps: list[str]
    expected_result: str
    source_document: str