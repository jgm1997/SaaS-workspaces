import logging
import uuid

from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

from app.api.deps import get_current_user
from app.core.abuse import is_blocked
from app.db.session import SessionLocal


class RequestIDMiddleWare(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        request_id = str(uuid.uuid4())
        request.state.request_id = request_id

        response: Response = await call_next(request)
        response.headers["X-Request-ID"] = request_id
        return response


class LoggingContextMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        request_id = getattr(request.state, "request_id", None)
        logger = logging.getLogger("app")

        extra = {"request_id": request_id}
        logger = logging.LoggerAdapter(logger, extra)

        request.state.logger = logger
        return await call_next(request)


class UserContextMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        db: Session = SessionLocal()
        try:
            try:
                user = await get_current_user(request, db)
                request.state.user = user
            except Exception:
                request.state.user = None
        finally:
            db.close()

        return await call_next(request)


class AbuseProtectionMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        ip = request.client.host
        if is_blocked(ip):
            return JSONResponse({"detail": "Too many requests"}, status_code=429)
        return await call_next(request)
