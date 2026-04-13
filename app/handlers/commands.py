from aiogram import Router, types
from aiogram.filters import Command
from datetime import datetime
import re
from aiogram.utils.keyboard import ReplyKeyboardBuilder
import httpx
import json
import config

router = Router()

# Создаем клавиатуру с кнопками меню
def get_menu_keyboard():
    builder = ReplyKeyboardBuilder()
    builder.button(text="🕒 Время")
    builder.button(text="ℹ️ Помощь")
    builder.button(text="🤖 Дикси")
    builder.button(text="🏠 Главное меню")
    builder.adjust(2, 2)  # 2 кнопки в каждом ряду
    return builder.as_markup(resize_keyboard=True)

async def ask_openrouter(prompt: str) -> str:
    """Отправляет запрос к OpenRouter API и возвращает ответ"""
    if not config.OPENROUTER_API_KEY:
        return "❌ Ошибка: API ключ OpenRouter не настроен. Добавьте OPENROUTER_API_KEY в .env файл."
    
    headers = {
        "Authorization": f"Bearer {config.OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://github.com/fuserwyn/ai_llm_shop",
        "X-Title": "AI LLM Shop Bot"
    }
    
    payload = {
        "model": config.OPENROUTER_MODEL,
        "messages": [
            {"role": "system", "content": "Ты Дикси - полезный AI ассистент в Telegram боте. Отвечай кратко и по делу."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.7,
        "max_tokens": 1000
    }
    
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(
                config.OPENROUTER_API_URL,
                headers=headers,
                json=payload
            )
            
            if response.status_code == 200:
                data = response.json()
                return data["choices"][0]["message"]["content"]
            else:
                return f"❌ Ошибка OpenRouter API: {response.status_code} - {response.text}"
    except httpx.RequestError as e:
        return f"❌ Ошибка подключения к OpenRouter: {str(e)}"
    except Exception as e:
        return f"❌ Неожиданная ошибка: {str(e)}"

@router.message(Command("help"))
async def cmd_help(message: types.Message):
    """Обработчик команды /help"""
    help_text = (
        "🤖 Доступные команды:\n\n"
        "/start - Начать работу с ботом\n"
        "/help - Показать это сообщение\n"
        "/time - Показать текущее время\n"
        "/dixi <текст> - Задать вопрос Дикси (AI ассистент)\n"
        "/openrouter <текст> - Альтернативная команда для Дикси\n"
        "/menu - Показать меню с кнопками"
    )
    await message.answer(help_text, reply_markup=get_menu_keyboard())

@router.message(Command("start"))
async def cmd_start(message: types.Message):
    """Обработчик команды /start"""
    welcome_text = (
        "👋 Добро пожаловать!\n\n"
        "Я бот для работы с AI/LLM моделями.\n"
        "Используйте кнопки ниже или команды для навигации.\n\n"
        "🤖 Теперь у меня есть Дикси - AI ассистент на базе OpenRouter!\n"
        "Используйте /dixi <вопрос> или кнопку \"Дикси\""
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

@router.message(Command("dixi"))
async def cmd_dixi(message: types.Message):
    """Обработчик команды /dixi - общение с AI ассистентом"""
    # Извлекаем текст после команды
    command_text = message.text
    prompt = command_text.replace('/dixi', '').strip()
    
    if not prompt:
        await message.answer("🤖 Дикси: Задайте ваш вопрос после команды /dixi\nНапример: /dixi Привет! Как дела?")
        return
    
    # Показываем статус обработки
    status_msg = await message.answer("🤖 Дикси думает...")
    
    # Отправляем запрос к OpenRouter
    response = await ask_openrouter(prompt)
    
    # Удаляем статус сообщение и отправляем ответ
    await status_msg.delete()
    await message.answer(f"🤖 Дикси:\n\n{response}")

@router.message(Command("openrouter"))
async def cmd_openrouter(message: types.Message):
    """Альтернативная команда для обращения к OpenRouter"""
    command_text = message.text
    prompt = command_text.replace('/openrouter', '').strip()
    
    if not prompt:
        await message.answer("🤖 OpenRouter: Задайте ваш вопрос после команды /openrouter")
        return
    
    # Перенаправляем в обработчик dixi
    await cmd_dixi(message)

@router.message(lambda message: message.text in ["🕒 Время", "ℹ️ Помощь", "🤖 Дикси", "🏠 Главное меню"])
async def handle_menu_buttons(message: types.Message):
    """Обработчик нажатий на кнопки меню"""
    if message.text == "🕒 Время":
        await cmd_time(message)
    elif message.text == "ℹ️ Помощь":
        await cmd_help(message)
    elif message.text == "🤖 Дикси":
        await message.answer("🤖 Дикси готов помочь! Напишите ваш вопрос:\n\nИспользуйте команду /dixi <ваш вопрос>")
    elif message.text == "🏠 Главное меню":
        await cmd_menu(message)

@router.message()
async def process_other_messages(message: types.Message):
    """Обработчик всех остальных сообщений"""
    # Игнорируем сообщения, которые не являются командами или кнопками меню
    pass