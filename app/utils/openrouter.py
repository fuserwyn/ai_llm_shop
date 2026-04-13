import httpx
import json
from typing import Dict, List, Optional
import config

async def get_available_models() -> List[Dict]:
    """Получить список доступных моделей из OpenRouter"""
    if not config.OPENROUTER_API_KEY:
        raise ValueError("OpenRouter API key not configured")
    
    headers = {
        "Authorization": f"Bearer {config.OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(
                f"{config.OPENROUTER_BASE_URL}/models",
                headers=headers,
                timeout=30.0
            )
            response.raise_for_status()
            data = response.json()
            return data.get("data", [])
        except httpx.HTTPStatusError as e:
            raise Exception(f"HTTP error: {e.response.status_code}")
        except Exception as e:
            raise Exception(f"Failed to fetch models: {str(e)}")

async def send_message_to_openrouter(
    message: str,
    model: Optional[str] = None,
    max_tokens: int = 1000
) -> Optional[str]:
    """Отправить сообщение в OpenRouter и получить ответ"""
    if not config.OPENROUTER_API_KEY:
        raise ValueError("OpenRouter API key not configured")
    
    model_to_use = model or config.DEFAULT_MODEL
    
    headers = {
        "Authorization": f"Bearer {config.OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://github.com/fuserwyn/ai_llm_shop",
        "X-Title": "AI LLM Shop Bot"
    }
    
    payload = {
        "model": model_to_use,
        "messages": [
            {
                "role": "user",
                "content": message
            }
        ],
        "max_tokens": max_tokens,
        "temperature": 0.7
    }
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                f"{config.OPENROUTER_BASE_URL}/chat/completions",
                headers=headers,
                json=payload,
                timeout=60.0
            )
            response.raise_for_status()
            data = response.json()
            
            if "choices" in data and len(data["choices"]) > 0:
                return data["choices"][0]["message"]["content"]
            else:
                return None
        except httpx.HTTPStatusError as e:
            error_text = f"HTTP error {e.response.status_code}"
            try:
                error_data = e.response.json()
                if "error" in error_data:
                    error_text = error_data["error"].get("message", error_text)
            except:
                pass
            raise Exception(error_text)
        except Exception as e:
            raise Exception(f"Failed to get response: {str(e)}")
