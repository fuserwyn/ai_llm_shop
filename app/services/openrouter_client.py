import httpx
import asyncio
from typing import List, Dict, Any, Optional
import config

class OpenRouterClient:
    """Клиент для работы с OpenRouter API"""
    
    def __init__(self):
        self.api_key = config.OPENROUTER_API_KEY
        self.base_url = config.OPENROUTER_BASE_URL
        self.model = config.OPENROUTER_MODEL
        self.deepseek_model = config.DEEPSEEK_MODEL
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://github.com/fuserwyn/ai_llm_shop",
            "X-Title": "AI LLM Shop Bot"
        }
    
    async def chat_completion(self, messages: List[Dict[str, str]], model: str = None, **kwargs) -> Optional[str]:
        """Отправляет запрос на завершение чата"""
        if not self.api_key:
            raise ValueError("OPENROUTER_API_KEY не установлен в конфигурации")
        
        # Используем указанную модель или модель по умолчанию
        target_model = model or self.model
        
        payload = {
            "model": target_model,
            "messages": messages,
            **kwargs
        }
        
        async with httpx.AsyncClient(timeout=30.0) as client:
            try:
                response = await client.post(
                    f"{self.base_url}/chat/completions",
                    headers=self.headers,
                    json=payload
                )
                
                response.raise_for_status()
                data = response.json()
                
                # Извлекаем текст ответа
                if data.get("choices") and len(data["choices"]) > 0:
                    return data["choices"][0]["message"]["content"]
                else:
                    return None
                    
            except httpx.HTTPStatusError as e:
                print(f"HTTP error: {e.response.status_code} - {e.response.text}")
                raise
            except Exception as e:
                print(f"Error in OpenRouter request: {e}")
                raise
    
    async def deepseek_completion(self, messages: List[Dict[str, str]], **kwargs) -> Optional[str]:
        """Отправляет запрос к DeepSeek модели"""
        return await self.chat_completion(messages, model=self.deepseek_model, **kwargs)
    
    async def get_models(self) -> List[Dict[str, Any]]:
        """Получает список доступных моделей"""
        if not self.api_key:
            raise ValueError("OPENROUTER_API_KEY не установлен в конфигурации")
        
        async with httpx.AsyncClient(timeout=30.0) as client:
            try:
                response = await client.get(
                    f"{self.base_url}/models",
                    headers=self.headers
                )
                
                response.raise_for_status()
                return response.json()["data"]
                
            except httpx.HTTPStatusError as e:
                print(f"HTTP error: {e.response.status_code} - {e.response.text}")
                raise
            except Exception as e:
                print(f"Error fetching models: {e}")
                raise

    async def check_balance(self) -> Optional[Dict[str, Any]]:
        """Проверяет баланс на OpenRouter"""
        if not self.api_key:
            raise ValueError("OPENROUTER_API_KEY не установлен в конфигурации")
        
        async with httpx.AsyncClient(timeout=30.0) as client:
            try:
                response = await client.get(
                    f"{self.base_url}/auth/key",
                    headers=self.headers
                )
                
                response.raise_for_status()
                return response.json()
                
            except httpx.HTTPStatusError as e:
                print(f"HTTP error: {e.response.status_code} - {e.response.text}")
                raise
            except Exception as e:
                print(f"Error checking balance: {e}")
                raise
