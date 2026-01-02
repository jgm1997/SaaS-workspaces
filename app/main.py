from fastapi import FastAPI

from app.api.v1.auth import router as auth_router
from app.api.v1.invitations import router as invitations_router
from app.api.v1.projects import router as projects_router
from app.api.v1.workspaces import router as workspaces_router
from app.core.logging import configure_logging
from app.core.middleware import LoggingContextMiddleware, RequestIDMiddleWare

configure_logging()

app = FastAPI(title="SaaS Workspaces API")

app.add_middleware(RequestIDMiddleWare)
app.add_middleware(LoggingContextMiddleware)

app.include_router(auth_router)
app.include_router(invitations_router)
app.include_router(projects_router)
app.include_router(workspaces_router)


@app.get("/health")
async def health_check():
    return {"status": "ok"}
