import logging
import time
import uuid

from fastapi import Request
from fastapi.responses import JSONResponse

logger = logging.getLogger(__name__)


async def log_requests(request: Request, call_next):
    """Log one request and attach its request ID to the response."""
    request_id = uuid.uuid4().hex[:8]
    request.state.request_id = request_id
    started = time.perf_counter()

    try:
        response = await call_next(request)
    except Exception:
        logger.exception("request_id=%s Unexpected request exception", request_id)
        response = JSONResponse(
            status_code=500,
            content={"detail": "Internal server error"},
        )

    duration_ms = (time.perf_counter() - started) * 1000
    message = (
        "request_id=%s %s %s status=%s duration=%.1fms",
        request_id,
        request.method,
        request.url.path,
        response.status_code,
        duration_ms,
    )
    if response.status_code >= 500:
        logger.error(*message)
    elif response.status_code >= 400:
        logger.warning(*message)
    else:
        logger.info(*message)

    response.headers["X-Request-ID"] = request_id
    return response
