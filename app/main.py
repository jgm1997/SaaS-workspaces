from fastapi import FastAPI

from app.api.v1.auth import router as auth_router
from app.api.v1.workspaces import router as workspaces_router

app = FastAPI(title="SaaS Workspaces API")
app.include_router(auth_router)
app.include_router(workspaces_router)


@app.get("/health")
async def health_check():
    return {"status": "ok"}
