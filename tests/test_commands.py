import pytest
from unittest.mock import AsyncMock, patch
from app.handlers.commands import cmd_help, cmd_start, cmd_time, process_other_messages, cmd_dixi, call_openrouter
from datetime import datetime

@pytest.mark.asyncio
async def test_cmd_help():
    message = AsyncMock()
    await cmd_help(message)
    message.answer.assert_called_once()
    assert "Доступные команды" in message.answer.call_args[0][0]
    assert "/time" in message.answer.call_args[0][0]
    assert "/dixi" in message.answer.call_args[0][0]

@pytest.mark.asyncio
async def test_cmd_start():
    message = AsyncMock()
    await cmd_start(message)
    message.answer.assert_called_once()
    assert "Добро пожаловать" in message.answer.call_args[0][0]
    assert "Dixi" in message.answer.call_args[0][0]

@pytest.mark.asyncio
async def test_cmd_time():
    message = AsyncMock()
    await cmd_time(message)
    message.answer.assert_called_once()
    response = message.answer.call_args[0][0]
    assert "Текущее время" in response
    # Проверяем, что в ответе есть форматированная дата
    assert any(month in response for month in [
        'января', 'февраля', 'марта', 'апреля', 'мая', 'июня',
        'июля', 'августа', 'сентября', 'октября', 'ноября', 'декабря'
    ])

@pytest.mark.asyncio
async def test_cmd_dixi_without_key():
    message = AsyncMock()
    # Мокаем конфиг без ключа
    with patch('app.handlers.commands.config.OPENROUTER_API_KEY', None):
        await cmd_dixi(message)
        message.answer.assert_called_once()
        assert "Ключ OpenRouter не настроен" in message.answer.call_args[0][0]

@pytest.mark.asyncio
async def test_cmd_dixi_with_key():
    message = AsyncMock()
    # Мокаем конфиг с ключом
    with patch('app.handlers.commands.config.OPENROUTER_API_KEY', 'test_key'):
        await cmd_dixi(message)
        message.answer.assert_called_once()
        assert "Dixi" in message.answer.call_args[0][0]
        assert "AI ассистент" in message.answer.call_args[0][0]

@pytest.mark.asyncio
async def test_call_openrouter_success():
    mock_response = {
        "choices": [
            {
                "message": {
                    "content": "Тестовый ответ от Dixi"
                }
            }
        ]
    }
    
    with patch('app.handlers.commands.config.OPENROUTER_API_KEY', 'test_key'), \
         patch('app.handlers.commands.httpx.AsyncClient') as mock_client:
        mock_async_client = AsyncMock()
        mock_client.return_value.__aenter__.return_value = mock_async_client
        mock_async_client.post.return_value = AsyncMock(status_code=200, json=AsyncMock(return_value=mock_response))
        
        result = await call_openrouter("Тестовый вопрос")
        assert result == "Тестовый ответ от Dixi"

@pytest.mark.asyncio
async def test_call_openrouter_error():
    with patch('app.handlers.commands.config.OPENROUTER_API_KEY', 'test_key'), \
         patch('app.handlers.commands.httpx.AsyncClient') as mock_client:
        mock_async_client = AsyncMock()
        mock_client.return_value.__aenter__.return_value = mock_async_client
        mock_async_client.post.return_value = AsyncMock(status_code=400, text="Bad Request")
        
        result = await call_openrouter("Тестовый вопрос")
        assert "Ошибка API" in result

@pytest.mark.asyncio
async def test_process_other_messages_with_dixi():
    message = AsyncMock()
    message.text = "Привет, как дела?"
    message.chat.id = 123
    
    with patch('app.handlers.commands.config.OPENROUTER_API_KEY', 'test_key'), \
         patch('app.handlers.commands.call_openrouter', AsyncMock(return_value="Всё отлично!")) as mock_dixi, \
         patch('app.handlers.commands.message.bot.send_chat_action', AsyncMock()) as mock_action:
        
        await process_other_messages(message)
        
        # Проверяем, что вызвался send_chat_action
        mock_action.assert_called_once_with(chat_id=123, action="typing")
        
        # Проверяем, что вызвался call_openrouter
        mock_dixi.assert_called_once_with("Привет, как дела?")
        
        # Проверяем, что ответ отправлен
        message.answer.assert_called_once()
        assert "Dixi" in message.answer.call_args[0][0]

@pytest.mark.asyncio
async def test_process_other_messages_without_key():
    message = AsyncMock()
    message.text = "Любое сообщение"
    
    with patch('app.handlers.commands.config.OPENROUTER_API_KEY', None):
        await process_other_messages(message)
        
        # Не должно вызывать answer для обычных сообщений без ключа
        message.answer.assert_not_called()