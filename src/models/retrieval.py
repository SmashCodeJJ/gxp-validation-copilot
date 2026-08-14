from pydantic import BaseModel


class RetrievedDocument(BaseModel):
    source_type: str
    source_id: str
    text: str
    source_document: str
    similarity_score: float