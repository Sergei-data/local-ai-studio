from fastapi import FastAPI
import httpx

from app.core.config import settings

app = FastAPI(title=settings.app_name)


@app.get("/")
def root() -> dict:
    return {
        "message": "Local AI Studio backend is running",
        "health": "/health",
        "ollama_health": "/ollama/health",
    }


@app.get("/health")
def health() -> dict:
    return {"status": "ok", "service": settings.app_name}


@app.get("/ollama/health")
async def ollama_health() -> dict:
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(f"{settings.ollama_base_url}/api/tags")
            response.raise_for_status()
            data = response.json()

        return {
            "status": "ok",
            "ollama_base_url": settings.ollama_base_url,
            "models_count": len(data.get("models", [])),
        }
    except Exception as exc:
        return {
            "status": "error",
            "ollama_base_url": settings.ollama_base_url,
            "detail": str(exc),
        }