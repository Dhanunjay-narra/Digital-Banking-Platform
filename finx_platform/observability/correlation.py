"""Correlation & Distributed Trace ID Context."""

import contextvars
import uuid

_correlation_id_ctx: contextvars.ContextVar[str] = contextvars.ContextVar("correlation_id", default="")
_user_id_ctx: contextvars.ContextVar[str] = contextvars.ContextVar("user_id", default="")


def get_correlation_id() -> str:
    cid = _correlation_id_ctx.get()
    if not cid:
        cid = f"finx-{uuid.uuid4().hex[:12]}"
        _correlation_id_ctx.set(cid)
    return cid


def set_correlation_id(cid: str) -> None:
    _correlation_id_ctx.set(cid)


def get_current_user_id() -> str:
    return _user_id_ctx.get()


def set_current_user_id(uid: str) -> None:
    _user_id_ctx.set(uid)
