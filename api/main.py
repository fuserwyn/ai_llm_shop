from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="AI Telegram Bot API")


class HealthResponse(BaseModel):
    status: str
    service: str


@app.get("/health")
async def health_check() -> HealthResponse:
    return HealthResponse(status="ok", service="ai-telegram-bot")


@app.get("/")
async def root():
    return {"message": "AI Telegram Bot API is running"}
