from fastapi import APIRouter, HTTPException, status

from app.orchestrator.task_orchestrator import TaskOrchestrator
from app.schemas.task import TaskCreate, TaskRead, build_task
from app.services.workspace_service import WorkspaceService

router = APIRouter(prefix="/tasks", tags=["tasks"])
workspace_service = WorkspaceService()
orchestrator = TaskOrchestrator()


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


@router.post("/{task_id}/run")
async def run_task(task_id: str) -> dict:
    task = workspace_service.get_task(task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return await orchestrator.run_task(task_id)


@router.get("/{task_id}/result")
def get_task_result(task_id: str) -> dict:
    task = workspace_service.get_task(task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")

    result = workspace_service.get_task_response(task_id)
    if result is None:
        raise HTTPException(status_code=404, detail="Task result not found")

    return {
        "task_id": task_id,
        "status": task.status,
        "content": result,
    }