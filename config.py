from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    BOT_TOKEN: str
    WEBHOOK_URL: str = ""  # e.g., "https://yourdomain.com/webhook"
    WEBHOOK_SECRET: str = "your_secret_token"
    WEBHOOK_PATH: str = "/webhook"
    WEBHOOK_HOST: str = "0.0.0.0"
    WEBHOOK_PORT: int = 8080
    
    class Config:
        env_file = ".env"


settings = Settings()
