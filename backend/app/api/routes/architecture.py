from fastapi import APIRouter

from app.schemas.architecture import ArchitectureDraft, ArchitectureRequest
from app.services.architecture_constructor import ArchitectureConstructorService

router = APIRouter(prefix="/architecture", tags=["architecture"])
service = ArchitectureConstructorService()


@router.post("/construct", response_model=ArchitectureDraft)
def construct_architecture(payload: ArchitectureRequest) -> ArchitectureDraft:
    return service.construct(payload)