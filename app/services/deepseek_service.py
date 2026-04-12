import logging
import aiohttp
from typing import Optional
from app.core.config import settings

logger = logging.getLogger(__name__)


class DeepSeekService:
    """Сервис для взаимодействия с DeepSeek AI API"""

    def __init__(self):
        self.api_key = settings.DEEPSEEK_API_KEY
        self.base_url = "https://api.deepseek.com/v1"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

    async def chat_completion(
        self,
        message: str,
        model: str = "deepseek-chat",
        max_tokens: int = 1000,
        temperature: float = 0.7
    ) -> Optional[str]:
        """
        Отправляет запрос к DeepSeek API и возвращает ответ.
        
        Args:
            message: Текст сообщения пользователя
            model: Модель DeepSeek (по умолчанию deepseek-chat)
            max_tokens: Максимальное количество токенов в ответе
            temperature: Креативность ответа (0.0-1.0)
        
        Returns:
            Текст ответа от AI или None в случае ошибки
        """
        if not self.api_key:
            logger.error("DeepSeek API key not configured")
            return None

        payload = {
            "model": model,
            "messages": [
                {"role": "user", "content": message}
            ],
            "max_tokens": max_tokens,
            "temperature": temperature
        }

        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.base_url}/chat/completions",
                    headers=self.headers,
                    json=payload,
                    timeout=aiohttp.ClientTimeout(total=30)
                ) as response:
                    
                    if response.status == 200:
                        data = await response.json()
                        return data["choices"][0]["message"]["content"]
                    else:
                        error_text = await response.text()
                        logger.error(
                            f"DeepSeek API error: {response.status} - {error_text}"
                        )
                        return None

        except aiohttp.ClientError as e:
            logger.error(f"Network error while calling DeepSeek API: {e}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error in DeepSeek service: {e}")
            return None


deepseek_service = DeepSeekService()