import logging

from fastapi import FastAPI

from src.api.exception_handlers import (
    unexpected_error_handler,
    value_error_handler,
)
from src.api.routes.agent import (
    router as agent_router,
)
from src.api.routes.health import (
    router as health_router,
)
from src.api.routes.rag import (
    router as rag_router,
)
from src.api.routes.validation import (
    router as validation_router,
)
from src.api.middleware.request_context import (
    RequestContextMiddleware,
)
from src.config.logging import configure_logging
from src.config.settings import get_settings

configure_logging()

logger = logging.getLogger("gxp.api")

settings = get_settings()


app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
)


app.add_exception_handler(
    ValueError,
    value_error_handler,
)

app.add_exception_handler(
    Exception,
    unexpected_error_handler,
)


app.include_router(
    health_router,
)

app.include_router(
    validation_router,
    prefix="/api/v1",
)

app.include_router(
    rag_router,
    prefix="/api/v1",
)

app.include_router(
    agent_router,
    prefix="/api/v1",
)

app.add_middleware(
    RequestContextMiddleware
)

logger.info(
    "Application initialized environment=%s",
    settings.environment,
)
