import pytest
from unittest.mock import AsyncMock, patch
from app.handlers.commands import cmd_help, cmd_start, cmd_time, process_other_messages
from datetime import datetime

@pytest.mark.asyncio
async def test_cmd_help():
    message = AsyncMock()
    await cmd_help(message)
    message.answer.assert_called_once()
    assert "Доступные команды" in message.answer.call_args[0][0]
    assert "/time" in message.answer.call_args[0][0]
    assert "/setdatetime" not in message.answer.call_args[0][0]

@pytest.mark.asyncio
async def test_cmd_start():
    message = AsyncMock()
    await cmd_start(message)
    message.answer.assert_called_once()
    assert "Добро пожаловать" in message.answer.call_args[0][0]

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
async def test_process_other_messages_with_dixi():
    message = AsyncMock()
    message.text = "любое сообщение"
    message.text.startswith = AsyncMock(return_value=False)
    
    with patch('app.handlers.commands.get_dixi_response', return_value="AI ответ"):
        await process_other_messages(message)
        message.answer.assert_called_once_with("AI ответ", reply_markup=AsyncMock())

@pytest.mark.asyncio
async def test_process_other_messages_ignore_command():
    message = AsyncMock()
    message.text = "/start"
    message.text.startswith = AsyncMock(return_value=True)
    
    await process_other_messages(message)
    message.answer.assert_not_called()

@pytest.mark.asyncio
async def test_process_other_messages_ignore_menu_button():
    message = AsyncMock()
    message.text = "🕒 Время"
    message.text.startswith = AsyncMock(return_value=False)
    
    await process_other_messages(message)
    message.answer.assert_not_called()