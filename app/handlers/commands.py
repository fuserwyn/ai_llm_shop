from aiogram import Router, types
from aiogram.filters import Command
from datetime import datetime
import re
from aiogram.utils.keyboard import InlineKeyboardBuilder

router = Router()

@router.message(Command("help"))
async def cmd_help(message: types.Message):
    """Обработчик команды /help"""
    help_text = (
        "🤖 Доступные команды:\n\n"
        "/start - Начать работу с ботом\n"
        "/help - Показать это сообщение\n"
        "/time - Показать текущее время\n"
        "Также вы можете использовать кнопки меню, которые появляются после /start\n"
        "# Добавьте другие команды по необходимости"
    )
    await message.answer(help_text)

@router.message(Command("start"))
async def cmd_start(message: types.Message):
    """Обработчик команды /start с инлайн-клавиатурой"""
    welcome_text = (
        "👋 Добро пожаловать!\n\n"
        "Я бот для работы с AI/LLM моделями.\n"
        "Используйте кнопки ниже или команды /help для списка команд."
    )
    
    # Создаем инлайн-клавиатуру
    builder = InlineKeyboardBuilder()
    builder.add(types.InlineKeyboardButton(text="🆘 Помощь", callback_data="help_button"))
    builder.add(types.InlineKeyboardButton(text="🕒 Время", callback_data="time_button"))
    builder.adjust(2)  # Две кнопки в ряд
    
    await message.answer(welcome_text, reply_markup=builder.as_markup())

@router.callback_query(lambda c: c.data == "help_button")
async def process_help_button(callback_query: types.CallbackQuery):
    """Обработчик нажатия кнопки Помощь"""
    help_text = (
        "🤖 Доступные команды:\n\n"
        "/start - Начать работу с ботом\n"
        "/help - Показать это сообщение\n"
        "/time - Показать текущее время\n"
        "Также вы можете использовать кнопки меню, которые появляются после /start\n"
        "# Добавьте другие команды по необходимости"
    )
    await callback_query.message.answer(help_text)
    await callback_query.answer()

@router.callback_query(lambda c: c.data == "time_button")
async def process_time_button(callback_query: types.CallbackQuery):
    """Обработчик нажатия кнопки Время"""
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
    await callback_query.message.answer(time_text)
    await callback_query.answer()

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
    # Игнорируем сообщения, которые не являются командами
    pass