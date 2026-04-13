import pytest
from unittest.mock import AsyncMock, patch
from app.handlers.commands import cmd_help, cmd_start, cmd_time, cmd_dixi, process_other_messages, ask_dixi
from datetime import datetime

@pytest.mark.asyncio
async def test_cmd_help():
    message = AsyncMock()
    await cmd_help(message)
    message.answer.assert_called_once()
    assert "Доступные команды" in message.answer.call_args[0][0]
    assert "/time" in message.answer.call_args[0][0]
    assert "/dixi" in message.answer.call_args[0][0]
    assert "/setdatetime" not in message.answer.call_args[0][0]

@pytest.mark.asyncio
async def test_cmd_start():
    message = AsyncMock()
    await cmd_start(message)
    message.answer.assert_called_once()
    assert "Добро пожаловать" in message.answer.call_args[0][0]
    assert "Дикси" in message.answer.call_args[0][0]

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
async def test_cmd_dixi():
    message = AsyncMock()
    await cmd_dixi(message)
    message.answer.assert_called_once()
    assert "Дикси готов к общению" in message.answer.call_args[0][0]
    assert "OpenRouter" in message.answer.call_args[0][0]

@pytest.mark.asyncio
async def test_process_other_messages_with_text():
    message = AsyncMock()
    message.text = "Привет, как дела?"
    message.chat.id = 123
    
    with patch('app.handlers.commands.ask_dixi', return_value="Привет! Я Дикси, всё отлично!") as mock_dixi:
        await process_other_messages(message)
        
        # Проверяем, что отправлено действие набора
        message.bot.send_chat_action.assert_called_once_with(123, "typing")
        # Проверяем, что вызван ask_dixi
        mock_dixi.assert_called_once_with("Привет, как дела?")
        # Проверяем, что отправлен ответ
        message.answer.assert_called_once()
        assert "Дикси" in message.answer.call_args[0][0]

@pytest.mark.asyncio
async def test_process_other_messages_with_command():
    message = AsyncMock()
    message.text = "/start"
    
    await process_other_messages(message)
    
    # Не должно вызывать answer для команд
    message.answer.assert_not_called()

@pytest.mark.asyncio
async def test_ask_dixi_success():
    mock_response = {
        "choices": [{
            "message": {
                "content": "Привет! Я Дикси."
            }
        }]
    }
    
    with patch('app.handlers.commands.config.OPENROUTER_API_KEY', 'test_key'), \
         patch('httpx.AsyncClient.post') as mock_post:
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = mock_response
        
        result = await ask_dixi("Привет")
        
        assert result == "Привет! Я Дикси."
        mock_post.assert_called_once()

@pytest.mark.asyncio
async def test_ask_dixi_no_api_key():
    with patch('app.handlers.commands.config.OPENROUTER_API_KEY', ''):
        result = await ask_dixi("Привет")
        
        assert "❌ Ключ OpenRouter не настроен" in result

@pytest.mark.asyncio
async def test_ask_dixi_api_error():
    with patch('app.handlers.commands.config.OPENROUTER_API_KEY', 'test_key'), \
         patch('httpx.AsyncClient.post') as mock_post:
        mock_post.return_value.status_code = 401
        mock_post.return_value.text = "Unauthorized"
        
        result = await ask_dixi("Привет")
        
        assert "❌ Ошибка OpenRouter" in result
        assert "401" in result
