from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    app_name: str = "local-ai-studio-backend"
    ollama_base_url: str = "http://host.docker.internal:11434"


settings = Settings()