"""Structured Banking Platform Logger."""

import logging
import sys
from datetime import datetime, timezone
from finx_platform.observability.correlation import get_correlation_id

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] [%(name)s] %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)]
)


class StructuredLogger:
    def __init__(self, name: str):
        self._logger = logging.getLogger(name)

    def info(self, msg: str, **kwargs):
        cid = get_correlation_id()
        extra_str = " ".join(f"{k}={v}" for k, v in kwargs.items())
        self._logger.info(f"[cid={cid}] {msg} {extra_str}".strip())

    def error(self, msg: str, **kwargs):
        cid = get_correlation_id()
        extra_str = " ".join(f"{k}={v}" for k, v in kwargs.items())
        self._logger.error(f"[cid={cid}] {msg} {extra_str}".strip())

    def warning(self, msg: str, **kwargs):
        cid = get_correlation_id()
        extra_str = " ".join(f"{k}={v}" for k, v in kwargs.items())
        self._logger.warning(f"[cid={cid}] {msg} {extra_str}".strip())

    def debug(self, msg: str, **kwargs):
        cid = get_correlation_id()
        extra_str = " ".join(f"{k}={v}" for k, v in kwargs.items())
        self._logger.debug(f"[cid={cid}] {msg} {extra_str}".strip())


def get_logger(name: str) -> StructuredLogger:
    return StructuredLogger(name)
