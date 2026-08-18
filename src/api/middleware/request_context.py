import logging
import uuid
from contextvars import ContextVar
from time import perf_counter

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware


logger = logging.getLogger("gxp.api.requests")

request_id_context: ContextVar[str] = ContextVar(
    "request_id",
    default="unknown",
)


def get_request_id() -> str:
    return request_id_context.get()


class RequestContextMiddleware(BaseHTTPMiddleware):

    async def dispatch(
        self,
        request: Request,
        call_next,
    ):
        request_id = request.headers.get(
            "X-Request-ID",
            str(uuid.uuid4()),
        )

        token = request_id_context.set(
            request_id
        )
        start_time = perf_counter()

        logger.info(
            "request_started request_id=%s method=%s path=%s",
            request_id,
            request.method,
            request.url.path,
        )

        try:
            response = await call_next(
                request
            )

            response.headers[
                "X-Request-ID"
            ] = request_id

            duration_ms = (
                perf_counter() - start_time
            ) * 1000

            logger.info(
                (
                    "request_completed method=%s path=%s "
                    "status_code=%s duration_ms=%.2f "
                    "request_id=%s"
                ),
                request.method,
                request.url.path,
                response.status_code,
                duration_ms,
                request_id,
            )

            return response

        except Exception:
            duration_ms = (
                perf_counter() - start_time
            ) * 1000

            logger.exception(
                (
                    "request_failed method=%s path=%s "
                    "duration_ms=%.2f request_id=%s"
                ),
                request.method,
                request.url.path,
                duration_ms,
                request_id,
            )

            raise

        finally:
            request_id_context.reset(
                token
            )
