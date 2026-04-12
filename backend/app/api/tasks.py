from fastapi import APIRouter, HTTPException, status

from app.schemas.task import TaskCreate, TaskRead, build_task
from app.services.workspace_service import WorkspaceService

router = APIRouter(prefix="/tasks", tags=["tasks"])
workspace_service = WorkspaceService()


@router.post("", response_model=TaskRead, status_code=status.HTTP_201_CREATED)
def create_task(payload: TaskCreate) -> TaskRead:
    task = build_task(payload)
    workspace_service.save_task(task)
    return task


@router.get("", response_model=list[TaskRead])
def list_tasks() -> list[TaskRead]:
    return workspace_service.list_tasks()


@router.get("/{task_id}", response_model=TaskRead)
def get_task(task_id: str) -> TaskRead:
    task = workspace_service.get_task(task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return task