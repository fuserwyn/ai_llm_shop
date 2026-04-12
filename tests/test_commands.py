import pytest
from unittest.mock import AsyncMock
from app.handlers.commands import cmd_help, cmd_start, cmd_setdatetime, process_datetime_input
from datetime import datetime

@pytest.mark.asyncio
async def test_cmd_help():
    message = AsyncMock()
    await cmd_help(message)
    message.answer.assert_called_once()
    assert "Доступные команды" in message.answer.call_args[0][0]
    assert "/setdatetime" in message.answer.call_args[0][0]

@pytest.mark.asyncio
async def test_cmd_start():
    message = AsyncMock()
    await cmd_start(message)
    message.answer.assert_called_once()
    assert "Добро пожаловать" in message.answer.call_args[0][0]

@pytest.mark.asyncio
async def test_cmd_setdatetime():
    message = AsyncMock()
    await cmd_setdatetime(message)
    message.answer.assert_called_once()
    assert "Введите текущую дату и время" in message.answer.call_args[0][0]
    assert "ГГГГ-ММ-ДД ЧЧ:ММ" in message.answer.call_args[0][0]

@pytest.mark.asyncio
async def test_process_datetime_input_valid():
    message = AsyncMock()
    message.text = "2023-10-15 14:30"
    
    await process_datetime_input(message)
    
    message.answer.assert_called_once()
    response = message.answer.call_args[0][0]
    assert "Дата и время установлены" in response
    assert "15 октября 2023 года, 14:30" in response

@pytest.mark.asyncio
async def test_process_datetime_input_invalid_format():
    message = AsyncMock()
    message.text = "неправильный формат"
    
    await process_datetime_input(message)
    
    # Не должно вызывать answer для неправильного формата
    message.answer.assert_not_called()

@pytest.mark.asyncio
async def test_process_datetime_input_invalid_date():
    message = AsyncMock()
    message.text = "2023-13-32 25:61"  # Некорректная дата
    
    await process_datetime_input(message)
    
    message.answer.assert_called_once()
    assert "Ошибка" in message.answer.call_args[0][0]
    assert "некорректная дата" in message.answer.call_args[0][0]