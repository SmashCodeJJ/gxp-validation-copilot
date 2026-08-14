from pydantic import BaseModel


class TraceabilityItem(BaseModel):
    requirement_id: str
    requirement_text: str
    explicitly_traced: bool
    test_ids: list[str]