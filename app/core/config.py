from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    # ... существующие настройки ...
    
    # DeepSeek API
    DEEPSEEK_API_KEY: Optional[str] = None
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()