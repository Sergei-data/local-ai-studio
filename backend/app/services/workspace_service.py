import json
from pathlib import Path
from datetime import datetime

from app.core.config import settings
from app.schemas.task import TaskRead


class WorkspaceService:
    def __init__(
        self,
        specs_dir: str | None = None,
        generated_dir: str | None = None,
    ) -> None:
        self.specs_dir = Path(specs_dir or settings.specs_dir)
        self.generated_dir = Path(generated_dir or settings.generated_dir)

        self.specs_dir.mkdir(parents=True, exist_ok=True)
        self.generated_dir.mkdir(parents=True, exist_ok=True)

    def _task_file(self, task_id: str) -> Path:
        return self.specs_dir / f"{task_id}.json"

    def _task_generated_dir(self, task_id: str) -> Path:
        path = self.generated_dir / task_id
        path.mkdir(parents=True, exist_ok=True)
        return path

    def task_response_file(self, task_id: str) -> Path:
        return self._task_generated_dir(task_id) / "response.md"

    def save_task(self, task: TaskRead) -> None:
        task_file = self._task_file(task.id)
        task_file.write_text(
            task.model_dump_json(indent=2),
            encoding="utf-8",
        )

    def update_task_status(self, task: TaskRead, status: str) -> TaskRead:
        updated = task.model_copy(
            update={
                "status": status,
                "updated_at": datetime.utcnow(),
            }
        )
        self.save_task(updated)
        return updated

    def get_task(self, task_id: str) -> TaskRead | None:
        task_file = self._task_file(task_id)
        if not task_file.exists():
            return None

        raw = task_file.read_text(encoding="utf-8")
        return TaskRead.model_validate_json(raw)

    def list_tasks(self) -> list[TaskRead]:
        tasks: list[TaskRead] = []

        for file_path in sorted(self.specs_dir.glob("*.json")):
            try:
                raw = file_path.read_text(encoding="utf-8")
                tasks.append(TaskRead.model_validate_json(raw))
            except (ValueError, json.JSONDecodeError):
                continue

        tasks.sort(key=lambda item: item.created_at, reverse=True)
        return tasks

    def save_task_response(self, task_id: str, content: str) -> Path:
        output_file = self.task_response_file(task_id)
        output_file.write_text(content, encoding="utf-8")
        return output_file

    def get_task_response(self, task_id: str) -> str | None:
        output_file = self.task_response_file(task_id)
        if not output_file.exists():
            return None
        return output_file.read_text(encoding="utf-8")