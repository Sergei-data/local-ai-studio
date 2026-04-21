from app.schemas.architecture import (
    ArchitectureDraft,
    ArchitectureRequest,
    ModuleContract,
)


class ArchitectureConstructorService:
    def construct(self, request: ArchitectureRequest) -> ArchitectureDraft:
        modules: list[str] = []
        tree: list[str] = []
        infra_files: list[str] = []
        steps: list[str] = []
        tests: list[str] = []
        contracts: list[ModuleContract] = []

        project_root = request.project_name.replace(" ", "_").lower()

        tree.extend(
            [
                f"{project_root}/",
                "├── backend/",
                "│   ├── app/",
                "│   │   ├── api/",
                "│   │   │   ├── deps.py",
                "│   │   │   ├── router.py",
                "│   │   │   └── v1/",
                "│   │   │       └── endpoints/",
                "│   │   ├── core/",
                "│   │   │   ├── config.py",
                "│   │   │   └── security.py",
                "│   │   ├── db/",
                "│   │   │   ├── base.py",
                "│   │   │   └── session.py",
                "│   │   ├── models/",
                "│   │   ├── schemas/",
                "│   │   ├── repositories/",
                "│   │   ├── services/",
                "│   │   └── main.py",
                "│   ├── tests/",
                "│   │   ├── unit/",
                "│   │   └── integration/",
                "│   ├── requirements.txt",
                "│   └── .env.example",
            ]
        )

        modules.extend(
            [
                "api",
                "core",
                "db",
                "models",
                "schemas",
                "repositories",
                "services",
            ]
        )

        contracts.extend(
            [
                ModuleContract(
                    module_name="config_core",
                    purpose="Хранение конфигурации приложения и security/settings слоя",
                    files=[
                        "backend/app/core/config.py",
                        "backend/app/core/security.py",
                    ],
                    inputs=["environment variables", "runtime settings"],
                    outputs=["application settings", "security utilities"],
                    dependencies=[],
                    tests=["config loading", "security helpers"],
                ),
                ModuleContract(
                    module_name="api_layer",
                    purpose="HTTP слой приложения с роутами, зависимостями и схемами запросов/ответов",
                    files=[
                        "backend/app/api/router.py",
                        "backend/app/api/deps.py",
                    ],
                    inputs=["HTTP requests", "authenticated user context"],
                    outputs=["HTTP responses"],
                    dependencies=["services", "schemas"],
                    tests=["endpoint integration tests", "validation tests"],
                ),
            ]
        )

        if request.migrations == "alembic":
            tree.extend(
                [
                    "│   ├── alembic/",
                    "│   │   ├── env.py",
                    "│   │   └── versions/",
                    "│   └── alembic.ini",
                ]
            )
            infra_files.extend(
                [
                    "backend/alembic.ini",
                    "backend/alembic/env.py",
                ]
            )
            modules.append("migrations")

        if request.database == "postgres":
            modules.append("postgres_db")
            contracts.append(
                ModuleContract(
                    module_name="database_layer",
                    purpose="Подключение к Postgres, session management и базовые db utilities",
                    files=[
                        "backend/app/db/base.py",
                        "backend/app/db/session.py",
                    ],
                    inputs=["DATABASE_URL"],
                    outputs=["db session", "base metadata"],
                    dependencies=["sqlalchemy", "models"],
                    tests=["db session initialization", "repository integration tests"],
                )
            )

        if request.storage != "none" or request.object_storage != "none":
            storage_kind = (
                request.object_storage if request.object_storage != "none" else request.storage
            )
            tree.extend(
                [
                    "│   ├── app/",
                    "│   │   └── integrations/",
                    "│   │       └── storage.py",
                ]
            )
            modules.append("storage")
            contracts.append(
                ModuleContract(
                    module_name="storage_integration",
                    purpose=f"Интеграция с object storage: {storage_kind}",
                    files=["backend/app/integrations/storage.py"],
                    inputs=["file bytes", "bucket/key metadata"],
                    outputs=["uploaded file metadata", "public/private urls"],
                    dependencies=["core.config"],
                    tests=["upload flow", "delete flow", "signed url flow"],
                )
            )

        if request.auth != "none":
            tree.extend(
                [
                    "│   ├── app/",
                    "│   │   ├── auth/",
                    "│   │   │   └── providers/",
                    "│   │   └── api/",
                    "│   │       └── v1/",
                    "│   │           └── endpoints/",
                    "│   │               └── auth.py",
                ]
            )
            modules.append("auth")
            contracts.append(
                ModuleContract(
                    module_name="auth_module",
                    purpose=f"Модуль аутентификации и авторизации через {request.auth}",
                    files=[
                        "backend/app/api/v1/endpoints/auth.py",
                        "backend/app/auth/providers/provider.py",
                    ],
                    inputs=["credentials", "access token", "user context"],
                    outputs=["authenticated principal", "access metadata"],
                    dependencies=["core.security", "api.deps"],
                    tests=["login flow", "permission checks", "protected endpoint tests"],
                )
            )

        if request.queue != "none":
            tree.extend(
                [
                    "│   ├── app/",
                    "│   │   ├── workers/",
                    "│   │   └── events/",
                ]
            )
            modules.extend(["queue", "workers"])
            contracts.append(
                ModuleContract(
                    module_name="event_processing",
                    purpose=f"Обработка фоновых событий через {request.queue}",
                    files=[
                        "backend/app/events/__init__.py",
                        "backend/app/workers/__init__.py",
                    ],
                    inputs=["domain events", "message payloads"],
                    outputs=["processed events", "side effects"],
                    dependencies=["services", "repositories"],
                    tests=["event publish tests", "worker processing tests"],
                )
            )

        if request.cache == "redis":
            tree.extend(
                [
                    "│   ├── app/",
                    "│   │   └── integrations/",
                    "│   │       └── cache.py",
                ]
            )
            modules.append("cache")
            contracts.append(
                ModuleContract(
                    module_name="cache_integration",
                    purpose="Кэширование данных и вычислений через Redis",
                    files=["backend/app/integrations/cache.py"],
                    inputs=["cache key", "value", "ttl"],
                    outputs=["cached value", "cache invalidation result"],
                    dependencies=["core.config"],
                    tests=["cache hit/miss tests", "cache invalidation tests"],
                )
            )

        if request.monitoring:
            tree.append("├── monitoring/")
            if "prometheus" in request.monitoring:
                tree.append("│   ├── prometheus/")
                infra_files.append("monitoring/prometheus/prometheus.yml")
            if "grafana" in request.monitoring:
                tree.append("│   ├── grafana/")
                infra_files.append("monitoring/grafana/")
            if "loki" in request.monitoring:
                tree.append("│   ├── loki/")
                infra_files.append("monitoring/loki/config.yml")
            modules.append("monitoring")

        if request.containerization in {"docker", "docker_compose"}:
            infra_files.extend(
                [
                    "backend.Dockerfile",
                    "frontend.Dockerfile",
                ]
            )
            if request.containerization == "docker_compose":
                infra_files.append("docker-compose.yml")

        if request.gateway == "nginx":
            infra_files.append("nginx/default.conf")

        tree.extend(
            [
                "├── frontend/",
                "│   ├── public/",
                "│   │   └── index.html",
                "│   └── assets/",
                "│       ├── css/",
                "│       ├── js/",
                "│       └── img/",
                "├── docs/",
                "├── workspace/",
                "│   ├── specs/",
                "│   ├── generated/",
                "│   ├── logs/",
                "│   └── artifacts/",
                "└── README.md",
            ]
        )

        steps.extend(
            [
                "Create project skeleton and configuration layer",
                "Create database/session/base setup",
                "Create domain models and Pydantic schemas",
                "Create repositories for persistence access",
                "Create service/use-case layer",
                "Create API endpoints and dependency wiring",
            ]
        )

        if request.auth != "none":
            steps.append("Add authentication and authorization layer")

        if request.storage != "none" or request.object_storage != "none":
            steps.append("Add object storage integration")

        if request.queue != "none":
            steps.append("Add event queue integration and workers")

        if request.cache != "none":
            steps.append("Add cache integration")

        if request.monitoring:
            steps.append("Add monitoring and observability stack")

        if request.containerization in {"docker", "docker_compose"}:
            steps.append("Generate infrastructure files and container setup")

        steps.extend(
            [
                "Create unit tests for business logic",
                "Create integration tests for API and infrastructure boundaries",
                "Validate contracts between modules",
            ]
        )

        tests.extend(
            [
                "Unit tests for service layer and business rules",
                "Integration tests for API endpoints",
            ]
        )

        if request.database != "none":
            tests.append("Integration tests for repositories and database session")

        if request.auth != "none":
            tests.append("Authentication and authorization tests")

        if request.storage != "none" or request.object_storage != "none":
            tests.append("Storage integration tests")

        if request.queue != "none":
            tests.append("Worker and event processing tests")

        if request.cache != "none":
            tests.append("Cache integration and invalidation tests")

        summary = (
            f"{request.backend_framework.upper()} {request.project_type} "
            f"with {request.architecture_style}, database={request.database}, "
            f"storage={request.storage}, object_storage={request.object_storage}, "
            f"auth={request.auth}, queue={request.queue}, cache={request.cache}, "
            f"containerization={request.containerization}, gateway={request.gateway}."
        )

        prompt_template = f"""Ты работаешь внутри утверждённой архитектуры проекта.

PROJECT CONTEXT:
- project_name: {request.project_name}
- project_type: {request.project_type}
- framework: {request.backend_framework}
- architecture_style: {request.architecture_style}
- database: {request.database}
- storage: {request.storage}
- object_storage: {request.object_storage}
- auth: {request.auth}
- queue: {request.queue}
- cache: {request.cache}
- migrations: {request.migrations}
- monitoring: {", ".join(request.monitoring) if request.monitoring else "none"}
- testing: {", ".join(request.testing) if request.testing else "none"}
- docs_mode: {request.docs_mode}

DOMAIN DESCRIPTION:
{request.description}

RULES:
- follow approved architecture
- do not invent unrelated modules
- keep separation between api, services, repositories, db, integrations
- generate only requested file/module
- follow file contract strictly
- output must match requested format exactly
"""

        return ArchitectureDraft(
            summary=summary,
            selected_modules=modules,
            directory_tree=tree,
            infra_files=infra_files,
            generation_steps=steps,
            test_strategy=tests,
            module_contracts=contracts,
            prompt_template=prompt_template,
        )