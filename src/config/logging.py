import logging
import sys

from src.api.middleware.request_context import (
    get_request_id,
)
from src.config.settings import get_settings


class RequestIdFilter(logging.Filter):

    def filter(
        self,
        record: logging.LogRecord,
    ) -> bool:

        record.request_id = (
            get_request_id()
        )

        return True


def configure_logging() -> None:

    settings = get_settings()

    handler = logging.StreamHandler(
        sys.stdout
    )

    handler.addFilter(
        RequestIdFilter()
    )

    formatter = logging.Formatter(
        "%(asctime)s "
        "%(levelname)s "
        "%(name)s "
        "request_id=%(request_id)s "
        "%(message)s"
    )

    handler.setFormatter(
        formatter
    )

    logging.basicConfig(
        level=getattr(
            logging,
            settings.log_level.upper(),
            logging.INFO,
        ),
        handlers=[handler],
        force=True,
    )