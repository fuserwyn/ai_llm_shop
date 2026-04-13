from aiogram import Router, types
from aiogram.filters import Command
from aiogram.filters.callback_data import CallbackData
from datetime import datetime
import re
from app.keyboards import main_menu_keyboard, help_keyboard

router = Router()

class MenuCallback(CallbackData, prefix="menu"):
    action: str

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
    await message.answer(help_text, reply_markup=help_keyboard())

@router.message(Command("start"))
async def cmd_start(message: types.Message):
    """Обработчик команды /start"""
    welcome_text = (
        "👋 Добро пожаловать!\n\n"
        "Я бот для работы с AI/LLM моделями.\n"
        "Используйте кнопки ниже для навигации."
    )
    await message.answer(welcome_text, reply_markup=main_menu_keyboard())

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
    await message.answer(time_text, reply_markup=main_menu_keyboard())

@router.callback_query(MenuCallback.filter())
async def process_menu_callback(callback_query: types.CallbackQuery, callback_data: MenuCallback):
    """Обработчик нажатий на кнопки меню"""
    action = callback_data.action
    
    if action == "help":
        help_text = (
            "🤖 Доступные команды:\n\n"
            "• /start - Начать работу с ботом\n"
            "• /help - Показать это сообщение\n"
            "• /time - Показать текущее время\n"
            "\nИспользуйте кнопки ниже для быстрого доступа к функциям."
        )
        await callback_query.message.edit_text(help_text, reply_markup=help_keyboard())
    elif action == "time":
        now = datetime.now()
        months = [
            'января', 'февраля', 'марта', 'апреля', 'мая', 'июня',
            'июля', 'августа', 'сентября', 'октября', 'ноября', 'декабря'
        ]
        day = now.day
        month_name = months[now.month - 1]
        year = now.year
        hour = now.hour
        minute = now.minute
        time_text = f"🕒 Текущее время: {day} {month_name} {year} года, {hour:02d}:{minute:02d}"
        await callback_query.message.edit_text(time_text, reply_markup=main_menu_keyboard())
    elif action == "main_menu":
        welcome_text = (
            "👋 Главное меню\n\n"
            "Я бот для работы с AI/LLM моделями.\n"
            "Используйте кнопки ниже для навигации."
        )
        await callback_query.message.edit_text(welcome_text, reply_markup=main_menu_keyboard())
    
    await callback_query.answer()

@router.message()
async def process_other_messages(message: types.Message):
    """Обработчик всех остальных сообщений"""
    # Если сообщение не команда, предлагаем меню
    if message.text and not message.text.startswith('/'):
        await message.answer("Используйте кнопки меню для навигации:", reply_markup=main_menu_keyboard())
