from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import aiohttp
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="AI LLM Shop Bot API")

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"


class ChatRequest(BaseModel):
    message: str


class ChatResponse(BaseModel):
    response: str


async def query_openrouter(prompt: str) -> str:
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": "openai/gpt-3.5-turbo",
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 500,
    }

    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(
                OPENROUTER_URL, headers=headers, json=payload
            ) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    return data["choices"][0]["message"]["content"].strip()
                else:
                    return f"API error: {resp.status}"
    except Exception as e:
        return f"Connection error: {e}"


@app.get("/")
async def root():
    return {"message": "AI LLM Shop Bot API is running"}


@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    if not request.message.strip():
        raise HTTPException(status_code=400, detail="Message cannot be empty")
    
    response = await query_openrouter(request.message)
    return ChatResponse(response=response)


@app.get("/health")
async def health_check():
    return {"status": "healthy"}
