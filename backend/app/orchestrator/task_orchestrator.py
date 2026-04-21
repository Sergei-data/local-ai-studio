from app.core.config import settings
from app.services.ollama_client import OllamaClient
from app.services.workspace_service import WorkspaceService


class TaskOrchestrator:
    def __init__(self) -> None:
        self.workspace = WorkspaceService()
        self.ollama = OllamaClient(model=settings.default_model)

    async def run_task(self, task_id: str) -> dict:
        task = self.workspace.get_task(task_id)
        if task is None:
            raise ValueError("Task not found")

        task = self.workspace.update_task_status(task, "running")

        system_prompt = (
            "Ты локальный AI coding assistant. "
            "Отвечай по задаче пользователя. "
            "Если просят код, старайся дать полезный, структурированный результат."
        )

        try:
            result = await self.ollama.generate(
                prompt=task.prompt,
                system=system_prompt,
            )

            output_file = self.workspace.save_task_response(task.id, result)
            task = self.workspace.update_task_status(task, "completed")

            return {
                "task_id": task.id,
                "status": task.status,
                "output_file": str(output_file),
                "result_preview": result[:1000],
            }
        except Exception as exc:
            task = self.workspace.update_task_status(task, "failed")
            return {
                "task_id": task.id,
                "status": task.status,
                "error": str(exc),
            }