from fastapi import FastAPI
import httpx

from app.api.routes.architecture import router as architecture_router
from app.api.routes.tasks import router as tasks_router
from app.api.routes.health import router as health_router
from app.core.config import settings

app = FastAPI(title=settings.app_name)

app.include_router(health_router)
app.include_router(tasks_router)
app.include_router(architecture_router)


@app.get("/")
def root() -> dict:
    return {
        "message": "Local AI Studio backend is running",
        "health": "/health",
        "ollama_health": "/ollama/health",
        "tasks": "/tasks",
        "architecture": "/architecture/construct",
    }