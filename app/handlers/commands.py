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
    builder.button(text="🏠 Главное меню")
    builder.button(text="🤖 Dixi")
    builder.adjust(2, 2)  # 2 кнопки в первом ряду, 2 во втором
    return builder.as_markup(resize_keyboard=True)

@router.message(Command("help"))
async def cmd_help(message: types.Message):
    """Обработчик команды /help"""
    help_text = (
        "🤖 Доступные команды:\n\n"
        "/start - Начать работу с ботом\n"
        "/help - Показать это сообщение\n"
        "/time - Показать текущее время\n"
        "/menu - Показать меню с кнопками\n"
        "/dixi - Поговорить с Dixi (AI ассистент)\n"
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
        "Теперь у меня есть Dixi - AI ассистент через OpenRouter!\n"
        "Напишите /dixi или нажмите кнопку 🤖 Dixi чтобы начать диалог."
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
    """Обработчик команды /dixi - начинает диалог с Dixi"""
    if not config.OPENROUTER_API_KEY:
        await message.answer("❌ Ключ OpenRouter не настроен. Обратитесь к администратору.")
        return
    
    welcome_dixi = (
        "🤖 Привет! Я Dixi - ваш AI ассистент через OpenRouter.\n\n"
        "Задайте мне любой вопрос, и я постараюсь помочь!\n"
        "Просто напишите сообщение, и я отвечу."
    )
    await message.answer(welcome_dixi, reply_markup=get_menu_keyboard())

async def call_openrouter(prompt: str) -> str:
    """Вызов OpenRouter API для получения ответа от Dixi"""
    if not config.OPENROUTER_API_KEY:
        return "Ошибка: Ключ API не настроен"
    
    headers = {
        "Authorization": f"Bearer {config.OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://github.com/fuserwyn/ai_llm_shop",
        "X-Title": "AI LLM Shop Bot"
    }
    
    data = {
        "model": config.OPENROUTER_MODEL,
        "messages": [
            {
                "role": "system",
                "content": "Ты - Dixi, дружелюбный AI ассистент в Telegram боте. Отвечай кратко и по делу. Будь полезным и вежливым."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        "max_tokens": 500,
        "temperature": 0.7
    }
    
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(
                config.OPENROUTER_API_URL,
                headers=headers,
                json=data
            )
            
            if response.status_code == 200:
                result = response.json()
                return result["choices"][0]["message"]["content"].strip()
            else:
                return f"Ошибка API: {response.status_code} - {response.text}"
    except Exception as e:
        return f"Ошибка соединения: {str(e)}"

@router.message(lambda message: message.text in ["🕒 Время", "ℹ️ Помощь", "🏠 Главное меню", "🤖 Dixi"])
async def handle_menu_buttons(message: types.Message):
    """Обработчик нажатий на кнопки меню"""
    if message.text == "🕒 Время":
        await cmd_time(message)
    elif message.text == "ℹ️ Помощь":
        await cmd_help(message)
    elif message.text == "🏠 Главное меню":
        await cmd_menu(message)
    elif message.text == "🤖 Dixi":
        await cmd_dixi(message)

@router.message()
async def process_other_messages(message: types.Message):
    """Обработчик всех остальных сообщений"""
    # Проверяем, не является ли сообщение командой или кнопкой меню
    if message.text and not message.text.startswith('/'):
        # Отправляем сообщение Dixi
        if config.OPENROUTER_API_KEY:
            # Показываем индикатор набора
            await message.bot.send_chat_action(chat_id=message.chat.id, action="typing")
            
            # Получаем ответ от OpenRouter
            response = await call_openrouter(message.text)
            
            # Отправляем ответ пользователю
            await message.answer(f"🤖 Dixi: {response}", reply_markup=get_menu_keyboard())
        else:
            # Если ключ не настроен, игнорируем сообщение
            pass