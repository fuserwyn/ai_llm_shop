from aiogram import Router, types
from aiogram.filters import Command
from aiogram.utils.keyboard import ReplyKeyboardBuilder
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
        "/time - Показать текущее время\n"
        "# Добавьте другие команды по необходимости"
    )
    builder = ReplyKeyboardBuilder()
    builder.row(types.KeyboardButton(text="🕒 Время"))
    builder.row(types.KeyboardButton(text="❓ Помощь"))
    builder.row(types.KeyboardButton(text="🚀 Старт"))
    keyboard = builder.as_markup(resize_keyboard=True)
    await message.answer(help_text, reply_markup=keyboard)

@router.message(Command("start"))
async def cmd_start(message: types.Message):
    """Обработчик команды /start"""
    welcome_text = (
        "👋 Добро пожаловать!\n\n"
        "Я бот для работы с AI/LLM моделями.\n"
        "Используйте кнопки ниже или /help для списка команд."
    )
    builder = ReplyKeyboardBuilder()
    builder.row(types.KeyboardButton(text="🕒 Время"))
    builder.row(types.KeyboardButton(text="❓ Помощь"))
    builder.row(types.KeyboardButton(text="🚀 Старт"))
    keyboard = builder.as_markup(resize_keyboard=True)
    await message.answer(welcome_text, reply_markup=keyboard)

@router.message(Command("time"))
async def cmd_time(message: types.Message):
    """Обработчик команды /time - показывает текущее время"""
    now = datetime.now()
    
    # Форматируем дату в читаемый вид
    months = [
        'января', 'февраля', 'марта', 'апреля', 'мая', 'июня',
        'июля', 'августа', 'сентября', 'октября', 'ноября', 'декабря'
    ]
    
    day = now.day
    month_name = months[now.month - 1]
    year = now.year
    hour = now.hour
    minute = now.minute
    
    time_text = (
        f"🕒 Текущее время: {day} {month_name} {year} года, {hour:02d}:{minute:02d}"
    )
    await message.answer(time_text)

@router.message()
async def process_other_messages(message: types.Message):
    """Обработчик всех остальных сообщений"""
    # Обработка нажатий кнопок
    if message.text == "🕒 Время":
        await cmd_time(message)
    elif message.text == "❓ Помощь":
        await cmd_help(message)
    elif message.text == "🚀 Старт":
        await cmd_start(message)
    else:
        # Игнорируем другие сообщения
        pass