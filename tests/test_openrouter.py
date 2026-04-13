import pytest
from unittest.mock import AsyncMock, patch, MagicMock
from app.services.openrouter_client import OpenRouterClient
import config

@pytest.mark.asyncio
async def test_openrouter_client_initialization():
    """Тест инициализации клиента OpenRouter"""
    client = OpenRouterClient()
    
    assert client.base_url == config.OPENROUTER_BASE_URL
    assert client.model == config.OPENROUTER_MODEL
    assert client.deepseek_model == config.DEEPSEEK_MODEL
    assert "Authorization" in client.headers
    assert "Content-Type" in client.headers

@pytest.mark.asyncio
async def test_chat_completion_success():
    """Тест успешного запроса к OpenRouter"""
    client = OpenRouterClient()
    
    mock_response = {
        "choices": [
            {
                "message": {
                    "content": "Привет! Я Дикси, ваш AI ассистент."
                }
            }
        ]
    }
    
    with patch("httpx.AsyncClient.post", new_callable=AsyncMock) as mock_post:
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = mock_response
        
        messages = [
            {"role": "user", "content": "Привет"}
        ]
        
        response = await client.chat_completion(messages)
        
        assert response == "Привет! Я Дикси, ваш AI ассистент."
        mock_post.assert_called_once()

@pytest.mark.asyncio
async def test_deepseek_completion():
    """Тест запроса к DeepSeek модели"""
    client = OpenRouterClient()
    
    mock_response = {
        "choices": [
            {
                "message": {
                    "content": "Привет! Я DeepSeek, мощная AI модель."
                }
            }
        ]
    }
    
    with patch("httpx.AsyncClient.post", new_callable=AsyncMock) as mock_post:
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = mock_response
        
        messages = [
            {"role": "user", "content": "Привет"}
        ]
        
        response = await client.deepseek_completion(messages)
        
        assert response == "Привет! Я DeepSeek, мощная AI модель."
        mock_post.assert_called_once()
        # Проверяем, что используется правильная модель
        call_args = mock_post.call_args
        assert call_args[1]['json']['model'] == config.DEEPSEEK_MODEL

@pytest.mark.asyncio
async def test_chat_completion_no_api_key():
    """Тест ошибки при отсутствии API ключа"""
    # Временно удаляем API ключ
    original_key = config.OPENROUTER_API_KEY
    config.OPENROUTER_API_KEY = None
    
    client = OpenRouterClient()
    
    with pytest.raises(ValueError, match="OPENROUTER_API_KEY не установлен"):
        messages = [
            {"role": "user", "content": "Привет"}
        ]
        await client.chat_completion(messages)
    
    # Восстанавливаем ключ
    config.OPENROUTER_API_KEY = original_key

@pytest.mark.asyncio
async def test_get_models():
    """Тест получения списка моделей"""
    client = OpenRouterClient()
    
    mock_models = {
        "data": [
            {"id": "openai/gpt-3.5-turbo", "name": "GPT-3.5 Turbo"},
            {"id": "openai/gpt-4", "name": "GPT-4"},
            {"id": "deepseek/deepseek-chat", "name": "DeepSeek Chat"},
            {"id": "deepseek/deepseek-coder", "name": "DeepSeek Coder"}
        ]
    }
    
    with patch("httpx.AsyncClient.get", new_callable=AsyncMock) as mock_get:
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = mock_models
        
        models = await client.get_models()
        
        assert len(models) == 4
        assert models[0]["id"] == "openai/gpt-3.5-turbo"
        assert models[2]["id"] == "deepseek/deepseek-chat"
        mock_get.assert_called_once()
