from fastapi import Request
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

from services.rate_limit_service import RateLimiter

from config.rate_limit import (
    RATE_LIMIT_REQUESTS,
    RATE_LIMIT_WINDOW
)


limiter = RateLimiter(
    RATE_LIMIT_REQUESTS,
    RATE_LIMIT_WINDOW
)


class RateLimitMiddleware(BaseHTTPMiddleware):

    async def dispatch(
        self,
        request: Request,
        call_next
    ):

        client = request.client.host

        allowed, data = limiter.check(client)

        if not allowed:

            return JSONResponse(
                status_code=429,
                content={
                    "detail": (
                        "Rate limit exceeded. "
                        "Try again later."
                    )
                }
            )

        response = await call_next(request)

        response.headers["X-RateLimit-Limit"] = str(
            RATE_LIMIT_REQUESTS
        )

        response.headers["X-RateLimit-Remaining"] = str(
            data["remaining"]
        )

        response.headers["X-RateLimit-Reset"] = str(
            data["reset"]
        )

        return response