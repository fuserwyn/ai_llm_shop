import pytest
from unittest.mock import AsyncMock
from app.handlers.commands import cmd_help, cmd_start, cmd_time
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
    assert "года" in response
    # Проверяем формат времени (часы:минуты)
    assert ":" in response
