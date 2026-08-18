from fastapi import (
    APIRouter,
    Depends,
    Response,
    status,
)
from sqlalchemy import text
from sqlalchemy.orm import Session

from src.api.dependencies import (
    get_database_session,
)
from src.config.settings import get_settings


router = APIRouter()


@router.get("/health")
def health() -> dict[str, str]:
    return {
        "status": "ok",
    }


@router.get("/version")
def version() -> dict[str, str]:
    settings = get_settings()

    return {
        "app_name": settings.app_name,
        "version": settings.app_version,
        "environment": settings.environment,
    }


@router.get("/ready")
def readiness(
    response: Response,
    session: Session = Depends(
        get_database_session
    ),
) -> dict[str, str]:

    try:
        session.execute(
            text("SELECT 1")
        )

        return {
            "status": "ready",
            "database": "ok",
        }

    except Exception:
        response.status_code = (
            status.HTTP_503_SERVICE_UNAVAILABLE
        )

        return {
            "status": "not_ready",
            "database": "unavailable",
        }
