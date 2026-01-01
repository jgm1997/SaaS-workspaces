from fastapi import FastAPI

app = FastAPI(title="SaaS Workspaces API")


@app.get("/health")
async def health_check():
    return {"status": "ok"}
