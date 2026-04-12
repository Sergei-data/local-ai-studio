from datetime import datetime
from typing import Literal
from uuid import uuid4

from pydantic import BaseModel, Field


TaskStatus = Literal["pending", "running", "failed", "completed"]


class TaskCreate(BaseModel):
    title: str = Field(..., min_length=3, max_length=200)
    prompt: str = Field(..., min_length=5)
    allowed_files: list[str] = Field(default_factory=list)
    task_type: str = Field(default="generate")


class TaskRead(BaseModel):
    id: str
    title: str
    prompt: str
    allowed_files: list[str]
    task_type: str
    status: TaskStatus
    created_at: datetime
    updated_at: datetime


def build_task(data: TaskCreate) -> TaskRead:
    now = datetime.utcnow()
    return TaskRead(
        id=str(uuid4()),
        title=data.title,
        prompt=data.prompt,
        allowed_files=data.allowed_files,
        task_type=data.task_type,
        status="pending",
        created_at=now,
        updated_at=now,
    )