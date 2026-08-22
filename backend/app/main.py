from fastapi import FastAPI

from backend.app.routers import router

app = FastAPI()

app.include_router(router, tags=["Actions"])


@app.get("/", tags=["Health Check"])
def health_check() -> dict[str, str]:
    return {"status": "ok", "project": "AI Quote Generator API", "version": "0.1.0"}
