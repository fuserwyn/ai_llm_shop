import pytest
from unittest.mock import AsyncMock, MagicMock
from app.handlers.commands import cmd_help, cmd_start, cmd_time, process_other_messages, process_menu_callback, MenuCallback
from datetime import datetime
from aiogram.types import CallbackQuery, Message
from aiogram.filters.callback_data import CallbackData

@pytest.mark.asyncio
async def test_cmd_help():
    message = AsyncMock()
    await cmd_help(message)
    message.answer.assert_called_once()
    assert "Доступные команды" in message.answer.call_args[0][0]
    assert "/time" in message.answer.call_args[0][0]
    assert message.answer.call_args[1].get("reply_markup") is not None

@pytest.mark.asyncio
async def test_cmd_start():
    message = AsyncMock()
    await cmd_start(message)
    message.answer.assert_called_once()
    assert "Добро пожаловать" in message.answer.call_args[0][0]
    assert message.answer.call_args[1].get("reply_markup") is not None

@pytest.mark.asyncio
async def test_cmd_time():
    message = AsyncMock()
    await cmd_time(message)
    message.answer.assert_called_once()
    response = message.answer.call_args[0][0]
    assert "Текущее время" in response
    assert message.answer.call_args[1].get("reply_markup") is not None
    # Проверяем, что в ответе есть форматированная дата
    assert any(month in response for month in [
        'января', 'февраля', 'марта', 'апреля', 'мая', 'июня',
        'июля', 'августа', 'сентября', 'октября', 'ноября', 'декабря'
    ])

@pytest.mark.asyncio
async def test_process_other_messages_with_text():
    message = AsyncMock()
    message.text = "любое сообщение"
    
    await process_other_messages(message)
    
    # Должно вызывать answer для обычных сообщений с предложением меню
    message.answer.assert_called_once()
    assert "Используйте кнопки меню" in message.answer.call_args[0][0]
    assert message.answer.call_args[1].get("reply_markup") is not None

@pytest.mark.asyncio
async def test_process_other_messages_with_command():
    message = AsyncMock()
    message.text = "/some_command"
    
    await process_other_messages(message)
    
    # Не должно вызывать answer для команд
    message.answer.assert_not_called()

@pytest.mark.asyncio
async def test_process_menu_callback_help():
    callback_query = AsyncMock()
    callback_query.message = AsyncMock()
    callback_data = MenuCallback(action="help")
    
    await process_menu_callback(callback_query, callback_data)
    
    callback_query.message.edit_text.assert_called_once()
    assert "Доступные команды" in callback_query.message.edit_text.call_args[0][0]
    callback_query.answer.assert_called_once()

@pytest.mark.asyncio
async def test_process_menu_callback_time():
    callback_query = AsyncMock()
    callback_query.message = AsyncMock()
    callback_data = MenuCallback(action="time")
    
    await process_menu_callback(callback_query, callback_data)
    
    callback_query.message.edit_text.assert_called_once()
    assert "Текущее время" in callback_query.message.edit_text.call_args[0][0]
    callback_query.answer.assert_called_once()

@pytest.mark.asyncio
async def test_process_menu_callback_main_menu():
    callback_query = AsyncMock()
    callback_query.message = AsyncMock()
    callback_data = MenuCallback(action="main_menu")
    
    await process_menu_callback(callback_query, callback_data)
    
    callback_query.message.edit_text.assert_called_once()
    assert "Главное меню" in callback_query.message.edit_text.call_args[0][0]
    callback_query.answer.assert_called_once()
