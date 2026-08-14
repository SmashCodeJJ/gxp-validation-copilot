import logging

from fastapi import Request
from fastapi.responses import JSONResponse


logger = logging.getLogger("gxp.api.errors")


async def value_error_handler(
    request: Request,
    exc: ValueError,
) -> JSONResponse:

    logger.warning(
        "Value error path=%s detail=%s",
        request.url.path,
        str(exc),
    )

    return JSONResponse(
        status_code=400,
        content={
            "error": "invalid_request",
            "detail": str(exc),
        },
    )


async def unexpected_error_handler(
    request: Request,
    exc: Exception,
) -> JSONResponse:

    logger.exception(
        "Unhandled exception path=%s",
        request.url.path,
    )

    return JSONResponse(
        status_code=500,
        content={
            "error": "internal_server_error",
            "detail": (
                "An unexpected server error occurred."
            ),
        },
    )