import json
from pathlib import Path

from app.schemas.task import TaskRead


class WorkspaceService:
    def __init__(self, specs_dir: str = "/workspace/specs") -> None:
        self.specs_dir = Path(specs_dir)
        self.specs_dir.mkdir(parents=True, exist_ok=True)

    def _task_file(self, task_id: str) -> Path:
        return self.specs_dir / f"{task_id}.json"

    def save_task(self, task: TaskRead) -> None:
        task_file = self._task_file(task.id)
        task_file.write_text(
            task.model_dump_json(indent=2),
            encoding="utf-8",
        )

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