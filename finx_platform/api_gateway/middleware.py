"""HTTP Middlewares for FinXCore API Gateway."""

import time
import uuid
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse, Response
from finx_platform.observability.correlation import set_correlation_id
from finx_platform.observability.logger import get_logger
from finx_platform.api_gateway.rate_limiter import rate_limiter
from finx_platform.common.exceptions import FinTechException

logger = get_logger("api_gateway.middleware")


class CorrelationAndLoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next) -> Response:
        # Extract or generate correlation ID
        correlation_id = request.headers.get("X-Correlation-ID", f"finx-{uuid.uuid4().hex[:12]}")
        set_correlation_id(correlation_id)

        # Rate limiting check
        client_ip = request.client.host if request.client else "127.0.0.1"
        if not rate_limiter.is_allowed(client_ip):
            return JSONResponse(
                status_code=429,
                content={
                    "error": "RATE_LIMIT_EXCEEDED",
                    "message": "Too many requests. Please slow down.",
                    "correlation_id": correlation_id
                }
            )

        start_time = time.time()
        try:
            response = await call_next(request)
            process_time = round((time.time() - start_time) * 1000, 2)
            response.headers["X-Correlation-ID"] = correlation_id
            response.headers["X-Response-Time-MS"] = str(process_time)
            return response
        except FinTechException as exc:
            process_time = round((time.time() - start_time) * 1000, 2)
            logger.warning(f"FinTech error: {exc.message}", code=exc.code, path=request.url.path)
            return JSONResponse(
                status_code=exc.status_code,
                content={
                    "success": False,
                    "error": exc.code,
                    "message": exc.message,
                    "details": exc.details,
                    "correlation_id": correlation_id,
                },
                headers={"X-Correlation-ID": correlation_id, "X-Response-Time-MS": str(process_time)}
            )
        except Exception as exc:
            process_time = round((time.time() - start_time) * 1000, 2)
            logger.error(f"Unhandled server error: {str(exc)}", path=request.url.path)
            return JSONResponse(
                status_code=500,
                content={
                    "success": False,
                    "error": "INTERNAL_SERVER_ERROR",
                    "message": "An unexpected error occurred during request processing.",
                    "correlation_id": correlation_id,
                },
                headers={"X-Correlation-ID": correlation_id, "X-Response-Time-MS": str(process_time)}
            )
