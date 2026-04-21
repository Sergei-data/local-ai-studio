from datetime import datetime
from uuid import uuid4

from pydantic import BaseModel, Field


class ModuleContract(BaseModel):
    module_name: str
    purpose: str
    files: list[str]
    inputs: list[str] = Field(default_factory=list)
    outputs: list[str] = Field(default_factory=list)
    dependencies: list[str] = Field(default_factory=list)
    tests: list[str] = Field(default_factory=list)


class ArchitectureRequest(BaseModel):
    project_name: str = Field(..., min_length=2, max_length=100)
    project_type: str = "backend"
    backend_framework: str = "fastapi"
    architecture_style: str = "clean_architecture"

    database: str = "postgres"
    storage: str = "none"
    object_storage: str = "none"
    auth: str = "none"
    queue: str = "none"
    cache: str = "none"

    monitoring: list[str] = Field(default_factory=list)
    migrations: str = "alembic"
    testing: list[str] = Field(default_factory=lambda: ["unit", "integration"])

    containerization: str = "docker_compose"
    gateway: str = "nginx"
    docs_mode: str = "official_docs"

    description: str = Field(..., min_length=10)


class ArchitectureDraft(BaseModel):
    summary: str
    selected_modules: list[str]
    directory_tree: list[str]
    infra_files: list[str]
    generation_steps: list[str]
    test_strategy: list[str]
    module_contracts: list[ModuleContract]
    prompt_template: str


class ArchitectureDraftRecord(BaseModel):
    id: str
    request: ArchitectureRequest
    draft: ArchitectureDraft
    created_at: datetime
    updated_at: datetime


def build_architecture_record(
    request: ArchitectureRequest,
    draft: ArchitectureDraft,
) -> ArchitectureDraftRecord:
    now = datetime.utcnow()
    return ArchitectureDraftRecord(
        id=str(uuid4()),
        request=request,
        draft=draft,
        created_at=now,
        updated_at=now,
    )