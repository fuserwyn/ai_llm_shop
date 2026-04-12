import pytest
from unittest.mock import AsyncMock
from app.handlers.commands import cmd_help, cmd_start, cmd_set_datetime

@pytest.mark.asyncio
async def test_cmd_help():
    message = AsyncMock()
    await cmd_help(message)
    message.answer.assert_called_once()
    assert "Доступные команды" in message.answer.call_args[0][0]
    assert "/set_datetime" in message.answer.call_args[0][0]

@pytest.mark.asyncio
async def test_cmd_start():
    message = AsyncMock()
    await cmd_start(message)
    message.answer.assert_called_once()
    assert "Добро пожаловать" in message.answer.call_args[0][0]

@pytest.mark.asyncio
async def test_cmd_set_datetime_valid():
    message = AsyncMock()
    message.text = "/set_datetime 2024-12-25 15:30:00"
    await cmd_set_datetime(message)
    message.answer.assert_called_once()
    assert "Дата и время установлены" in message.answer.call_args[0][0]
    assert "25.12.2024" in message.answer.call_args[0][0]
    assert "15:30:00" in message.answer.call_args[0][0]

@pytest.mark.asyncio
async def test_cmd_set_datetime_invalid_format():
    message = AsyncMock()
    message.text = "/set_datetime 2024-12-25"  # Не хватает времени
    await cmd_set_datetime(message)
    message.answer.assert_called_once()
    assert "Неверный формат команды" in message.answer.call_args[0][0]
    assert "Пример" in message.answer.call_args[0][0]

@pytest.mark.asyncio
async def test_cmd_set_datetime_invalid_date():
    message = AsyncMock()
    message.text = "/set_datetime 2024-13-25 15:30:00"  # Неверный месяц
    await cmd_set_datetime(message)
    message.answer.assert_called_once()
    assert "Ошибка парсинга" in message.answer.call_args[0][0]
    assert "Проверьте формат" in message.answer.call_args[0][0]