from aiogram import Router, types
from aiogram.filters import Command
from datetime import datetime
import re

router = Router()

@router.message(Command("help"))
async def cmd_help(message: types.Message):
    """Обработчик команды /help"""
    help_text = (
        "🤖 Доступные команды:\n\n"
        "/start - Начать работу с ботом\n"
        "/help - Показать это сообщение\n"
        "/setdatetime - Установить дату и время\n"
        "# Добавьте другие команды по необходимости"
    )
    await message.answer(help_text)

@router.message(Command("start"))
async def cmd_start(message: types.Message):
    """Обработчик команды /start"""
    welcome_text = (
        "👋 Добро пожаловать!\n\n"
        "Я бот для работы с AI/LLM моделями.\n"
        "Используйте /help для списка команд."
    )
    await message.answer(welcome_text)

@router.message(Command("setdatetime"))
async def cmd_setdatetime(message: types.Message):
    """Обработчик команды /setdatetime - запрашивает ввод даты и времени"""
    request_text = (
        "Введите текущую дату и время в формате ГГГГ-ММ-ДД ЧЧ:ММ\n"
        "Например: 2023-10-15 14:30"
    )
    await message.answer(request_text)

@router.message()
async def process_datetime_input(message: types.Message):
    """Обработчик ввода даты и времени после команды /setdatetime"""
    # Проверяем, соответствует ли сообщение формату даты и времени
    pattern = r'^\d{4}-\d{2}-\d{2} \d{2}:\d{2}$'
    
    if re.match(pattern, message.text.strip()):
        try:
            # Парсим дату и время
            dt = datetime.strptime(message.text.strip(), '%Y-%m-%d %H:%M')
            
            # Форматируем дату в читаемый вид
            months = [
                'января', 'февраля', 'марта', 'апреля', 'мая', 'июня',
                'июля', 'августа', 'сентября', 'октября', 'ноября', 'декабря'
            ]
            
            day = dt.day
            month_name = months[dt.month - 1]
            year = dt.year
            hour = dt.hour
            minute = dt.minute
            
            response_text = (
                f"Дата и время установлены: {day} {month_name} {year} года, {hour:02d}:{minute:02d}"
            )
            await message.answer(response_text)
            
        except ValueError:
            await message.answer("Ошибка: введена некорректная дата или время. Попробуйте снова.")
    else:
        # Игнорируем сообщения, которые не являются ответом на запрос даты/времени
        # (этот обработчик будет реагировать только на сообщения с правильным форматом)
        pass