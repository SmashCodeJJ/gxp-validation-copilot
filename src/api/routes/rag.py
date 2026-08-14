from typing import Annotated

from fastapi import (
    APIRouter,
    Depends,
)
from sqlalchemy.orm import Session

from src.api.dependencies import (
    get_database_session,
    get_rag_service,
)
from src.models.rag import RagAnswer
from src.models.rag_request import RagQuestion
from src.services.rag_service import RagService


router = APIRouter(
    prefix="/rag",
    tags=["RAG"],
)


@router.post(
    "/query",
    response_model=RagAnswer,
)
def rag_query(
    request: RagQuestion,
    session: Annotated[
        Session,
        Depends(get_database_session),
    ],
    rag_service: Annotated[
        RagService,
        Depends(get_rag_service),
    ],
):
    return rag_service.answer_question(
        session=session,
        question=request.question,
    )