from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/humanitaid"
    stripe_api_key: str = ""
    stripe_webhook_secret: str = ""
    smtp_host: str = ""
    smtp_port: int = 587
    smtp_user: str = ""
    smtp_password: str = ""
    smtp_from: str = "noreply@humanitaid.org"
    app_name: str = "HumanitAID"
    debug: bool = False
    secret_key: str = "change-me-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 1440

    model_config = {"env_file": ".env", "env_file_encoding": "utf-8"}


settings = Settings()
