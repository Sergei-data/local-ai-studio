from fastapi import APIRouter
import httpx

from app.core.config import settings

router = APIRouter(tags=["health"])


@router.get("/health")
def health() -> dict:
    return {"status": "ok", "service": settings.app_name}


@router.get("/ollama/health")
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