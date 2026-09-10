from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Runtime settings. LLM keys are optional; the API must work without them."""

    model_config = SettingsConfigDict(env_prefix="DESKFLOW_", extra="ignore")

    llm_api_key: str = ""
    llm_base_url: str = "https://api.openai.com/v1"
    llm_model: str = "gpt-4o-mini"
    llm_timeout_seconds: float = 12.0
    database_url: str = "sqlite:///data/deskflow.sqlite"
    env: str = "dev"

    def llm_enabled(self) -> bool:
        return bool(self.llm_api_key.strip())

    def show_sample_logins(self) -> bool:
        return self.env.strip().lower() in {"dev", "test"}


def get_settings() -> Settings:
    return Settings()
