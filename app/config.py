from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    bot_token: str
    admin_ids: list[int]
    database_url: str
    redis_url: str
    openai_api_key: str
    yookassa_shop_id: str
    yookassa_secret_key: str
    webhook_url: str
    webhook_path: str
    host: str
    port: int

    class Config:
        env_file = ".env"


settings = Settings()