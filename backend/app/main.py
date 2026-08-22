from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.routers import router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.FRONTEND_URL],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router, tags=["Actions"])


@app.get("/", tags=["Health Check"])
def health_check() -> dict[str, str]:
    return {"status": "ok", "project": "AI Quote Generator API", "version": "0.1.0"}
