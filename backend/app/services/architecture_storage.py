import json
from pathlib import Path

from app.schemas.architecture import ArchitectureDraftRecord


class ArchitectureStorageService:
    def __init__(self, base_dir: str = "/workspace/specs/architectures") -> None:
        self.base_dir = Path(base_dir)
        self.base_dir.mkdir(parents=True, exist_ok=True)

    def _file(self, draft_id: str) -> Path:
        return self.base_dir / f"{draft_id}.json"

    def save(self, record: ArchitectureDraftRecord) -> None:
        self._file(record.id).write_text(
            record.model_dump_json(indent=2),
            encoding="utf-8",
        )

    def get(self, draft_id: str) -> ArchitectureDraftRecord | None:
        file_path = self._file(draft_id)
        if not file_path.exists():
            return None
        return ArchitectureDraftRecord.model_validate_json(
            file_path.read_text(encoding="utf-8")
        )

    def list_all(self) -> list[ArchitectureDraftRecord]:
        items: list[ArchitectureDraftRecord] = []

        for file_path in sorted(self.base_dir.glob("*.json")):
            try:
                items.append(
                    ArchitectureDraftRecord.model_validate_json(
                        file_path.read_text(encoding="utf-8")
                    )
                )
            except (ValueError, json.JSONDecodeError):
                continue

        items.sort(key=lambda item: item.created_at, reverse=True)
        return items