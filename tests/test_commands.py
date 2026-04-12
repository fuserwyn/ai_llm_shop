import pytest
from unittest.mock import AsyncMock
from app.handlers.commands import cmd_help, cmd_start

@pytest.mark.asyncio
async def test_cmd_help():
    message = AsyncMock()
    await cmd_help(message)
    message.answer.assert_called_once()
    assert "Доступные команды" in message.answer.call_args[0][0]

@pytest.mark.asyncio
async def test_cmd_start():
    message = AsyncMock()
    await cmd_start(message)
    message.answer.assert_called_once()
    assert "Добро пожаловать" in message.answer.call_args[0][0]
