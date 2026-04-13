from aiogram import Router, types
from aiogram.filters import Command
from datetime import datetime
import re
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from app.services.openrouter_client import OpenRouterClient

router = Router()

# Создаем клавиатуру с кнопками меню
def get_menu_keyboard():
    builder = ReplyKeyboardBuilder()
    builder.button(text="🕒 Время")
    builder.button(text="ℹ️ Помощь")
    builder.button(text="🔍 DeepSeek")
    builder.button(text="🏠 Главное меню")
    builder.adjust(2, 2)  # 2 кнопки в каждом ряду
    return builder.as_markup(resize_keyboard=True)

@router.message(Command("help"))
async def cmd_help(message: types.Message):
    """Обработчик команды /help"""
    help_text = (
        "🤖 Доступные команды:\n\n"
        "/start - Начать работу с ботом\n"
        "/help - Показать это сообщение\n"
        "/time - Показать текущее время\n"
        "/deepseek - Задать вопрос DeepSeek модели\n"
        "/menu - Показать меню с кнопками\n"
        "# Добавьте другие команды по необходимости"
    )
    await message.answer(help_text, reply_markup=get_menu_keyboard())

@router.message(Command("start"))
async def cmd_start(message: types.Message):
    """Обработчик команды /start"""
    welcome_text = (
        "👋 Добро пожаловать!\n\n"
        "Я бот для работы с AI/LLM моделями.\n"
        "Используйте кнопки ниже или команды для навигации.\n\n"
        "Теперь доступны:\n"
        "• DeepSeek - мощная модель для сложных задач!\n\n"
        "Используйте команду /deepseek"
    )
    await message.answer(welcome_text, reply_markup=get_menu_keyboard())

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
    await message.answer(time_text, reply_markup=get_menu_keyboard())

@router.message(Command("menu"))
async def cmd_menu(message: types.Message):
    """Обработчик команды /menu - показывает меню с кнопками"""
    menu_text = "📱 Выберите действие из меню ниже:"
    await message.answer(menu_text, reply_markup=get_menu_keyboard())

@router.message(Command("deepseek"))
async def cmd_deepseek(message: types.Message):
    """Обработчик команды /deepseek - начинает работу с DeepSeek"""
    instruction_text = (
        "🔍 DeepSeek готов к работе!\n\n"
        "Отправьте мне любой запрос, и я передам его модели DeepSeek через OpenRouter.\n\n"
        "DeepSeek отлично справляется с:\n"
        "• Сложными техническими вопросами\n"
        "• Анализом кода и алгоритмов\n"
        "• Научными и исследовательскими задачами\n"
        "• Логическими рассуждениями\n\n"
        "Задайте ваш вопрос..."
    )
    await message.answer(instruction_text, reply_markup=get_menu_keyboard())

@router.message(lambda message: message.text in ["🕒 Время", "ℹ️ Помощь", "🔍 DeepSeek", "🏠 Главное меню"])
async def handle_menu_buttons(message: types.Message):
    """Обработчик нажатий на кнопки меню"""
    if message.text == "🕒 Время":
        await cmd_time(message)
    elif message.text == "ℹ️ Помощь":
        await cmd_help(message)
    elif message.text == "🔍 DeepSeek":
        await cmd_deepseek(message)
    elif message.text == "🏠 Главное меню":
        await cmd_menu(message)

@router.message()
async def process_other_messages(message: types.Message):
    """Обработчик всех остальных сообщений"""
    # Если это не команда и не кнопка меню, отправляем в DeepSeek
    try:
        # Инициализируем клиент OpenRouter
        client = OpenRouterClient()
        
        # Отправляем сообщение пользователя в DeepSeek
        response = await client.chat_completion(
            messages=[
                {
                    "role": "system",
                    "content": "Ты - DeepSeek, мощная AI модель. Отвечай на русском языке, будь точным и информативным. Предоставляй развернутые ответы на сложные вопросы."
                },
                {
                    "role": "user",
                    "content": message.text
                }
            ],
            model="deepseek/deepseek-chat"  # Указываем модель DeepSeek
        )
        
        if response:
            await message.answer(f"🔍 DeepSeek: {response}", reply_markup=get_menu_keyboard())
        else:
            await message.answer("⚠️ Извините, DeepSeek временно недоступен. Попробуйте позже.", reply_markup=get_menu_keyboard())
    
    except Exception as e:
        await message.answer(f"❌ Ошибка при обращении к DeepSeek: {str(e)}", reply_markup=get_menu_keyboard())

@router.message(lambda message: message.text and message.text.startswith("/deepseek_"))
async def process_deepseek_query(message: types.Message):
    """Обработчик прямых запросов к DeepSeek через команду"""
    query = message.text.replace("/deepseek_", "", 1).strip()
    if not query:
        await message.answer("🔍 Пожалуйста, укажите запрос после команды /deepseek_")
        return
    
    try:
        client = OpenRouterClient()
        
        # Используем модель DeepSeek через OpenRouter
        response = await client.chat_completion(
            messages=[
                {
                    "role": "system",
                    "content": "Ты - DeepSeek, мощная AI модель. Отвечай на русском языке, будь точным и информативным. Предоставляй развернутые ответы на сложные вопросы."
                },
                {
                    "role": "user",
                    "content": query
                }
            ],
            model="deepseek/deepseek-chat"  # Указываем модель DeepSeek
        )
        
        if response:
            await message.answer(f"🔍 DeepSeek: {response}", reply_markup=get_menu_keyboard())
        else:
            await message.answer("⚠️ Извините, DeepSeek временно недоступен. Попробуйте позже.", reply_markup=get_menu_keyboard())
    
    except Exception as e:
        await message.answer(f"❌ Ошибка при обращении к DeepSeek: {str(e)}", reply_markup=get_menu_keyboard())
