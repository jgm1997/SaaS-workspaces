import logging
import sys

from pythonjsonlogger import jsonlogger


class RequestIDFilter(logging.Filter):
    def filter(self, record):
        record.request_id = getattr(record, "request_id", None)
        return True


def configure_logging() -> None:
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    handler = logging.StreamHandler(sys.stdout)
    formatter = jsonlogger.JsonFormatter(
        "%(asctime)s %(levelname)s %(name)s %(message)s %(request_id)s"
    )
    handler.setFormatter(formatter)
    handler.addFilter(RequestIDFilter())
    logger.handlers = [handler]
