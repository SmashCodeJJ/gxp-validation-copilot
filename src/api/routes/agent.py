from typing import Annotated

from fastapi import (
    APIRouter,
    Depends,
)
from sqlalchemy.orm import Session

from src.agent.models import (
    AgentRequest,
    AgentResponse,
)
from src.agent.service import AgentService
from src.api.dependencies import (
    get_agent_service,
    get_database_session,
)


router = APIRouter(
    prefix="/agent",
    tags=["Agent"],
)


@router.post(
    "/query",
    response_model=AgentResponse,
)
def agent_query(
    request: AgentRequest,
    session: Annotated[
        Session,
        Depends(get_database_session),
    ],
    agent_service: Annotated[
        AgentService,
        Depends(get_agent_service),
    ],
):
    return agent_service.answer(
        session=session,
        question=request.question,
    )
