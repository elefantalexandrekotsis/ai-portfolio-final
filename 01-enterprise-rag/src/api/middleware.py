import time, logging
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request

logger = logging.getLogger(__name__)

class RequestLoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        t = time.time()
        response = await call_next(request)
        ms = (time.time()-t)*1000
        logger.info(f"{request.method} {request.url.path} -> {response.status_code} ({ms:.0f}ms)")
        response.headers["X-Response-Time-Ms"] = str(round(ms,2))
        return response
