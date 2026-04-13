import httpx
import config
import logging

logger = logging.getLogger(__name__)

async def get_dixi_response(user_message: str) -> str:
    """Получает ответ от OpenRouter API через Dixi"""
    if not config.OPENROUTER_API_KEY:
        return "⚠️ API ключ OpenRouter не настроен. Добавьте OPENROUTER_API_KEY в .env файл."
    
    headers = {
        "Authorization": f"Bearer {config.OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://github.com/fuserwyn/ai_llm_shop",
        "X-Title": "AI LLM Shop Bot"
    }
    
    payload = {
        "model": config.OPENROUTER_MODEL,
        "messages": [
            {
                "role": "user",
                "content": user_message
            }
        ],
        "max_tokens": -1
    }
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{config.OPENROUTER_API_URL}/chat/completions",
                headers=headers,
                json=payload,
                timeout=30.0
            )
            
            if response.status_code == 200:
                data = response.json()
                return data["choices"][0]["message"]["content"]
            else:
                logger.error(f"OpenRouter API error: {response.status_code} - {response.text}")
                return "⚠️ Ошибка при обращении к AI. Попробуйте позже."
    except httpx.RequestError as e:
        logger.error(f"Request error: {e}")
        return "⚠️ Ошибка сети. Попробуйте позже."
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        return "⚠️ Неожиданная ошибка. Попробуйте позже."