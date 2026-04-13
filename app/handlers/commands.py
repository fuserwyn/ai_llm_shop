from aiogram import Router, types
from aiogram.filters import Command
from datetime import datetime
import re
from aiogram.utils.keyboard import ReplyKeyboardBuilder
import httpx
import config
import json

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

async def ask_dixi(user_message: str) -> str:
    """Отправляет запрос к OpenRouter API через Dixi"""
    if not config.OPENROUTER_API_KEY:
        return "❌ Ключ OpenRouter не настроен. Обратитесь к администратору."
    
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
            {"role": "user", "content": user_message}
        ],
        "max_tokens": 500
    }
    
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(
                f"{config.OPENROUTER_BASE_URL}/chat/completions",
                headers=headers,
                json=payload
            )
            
            if response.status_code == 200:
                data = response.json()
                return data["choices"][0]["message"]["content"]
            else:
                return f"❌ Ошибка OpenRouter: {response.status_code} - {response.text}"
    except Exception as e:
        return f"❌ Ошибка соединения: {str(e)}"

@router.message(Command("help"))
async def cmd_help(message: types.Message):
    """Обработчик команды /help"""
    help_text = (
        "🤖 Доступные команды:\n\n"
        "/start - Начать работу с ботом\n"
        "/help - Показать это сообщение\n"
        "/time - Показать текущее время\n"
        "/dixi - Поговорить с AI ассистентом Дикси\n"
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
        "🤖 Для общения с AI ассистентом Дикси используйте команду /dixi или кнопку ниже."
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
    """Обработчик команды /dixi - начинает диалог с Дикси"""
    dixi_text = (
        "🤖 Дикси готов к общению!\n\n"
        "Отправьте мне сообщение, и я передам его AI ассистенту Дикси.\n"
        "Дикси подключен через OpenRouter API."
    )
    await message.answer(dixi_text, reply_markup=get_menu_keyboard())

@router.message(lambda message: message.text in ["🕒 Время", "ℹ️ Помощь", "🤖 Дикси", "🏠 Главное меню"])
async def handle_menu_buttons(message: types.Message):
    """Обработчик нажатий на кнопки меню"""
    if message.text == "🕒 Время":
        await cmd_time(message)
    elif message.text == "ℹ️ Помощь":
        await cmd_help(message)
    elif message.text == "🤖 Дикси":
        await cmd_dixi(message)
    elif message.text == "🏠 Главное меню":
        await cmd_menu(message)

@router.message()
async def process_other_messages(message: types.Message):
    """Обработчик всех остальных сообщений"""
    # Если это ответ на предыдущее сообщение Дикси или просто текст
    if message.text and not message.text.startswith('/'):
        # Показываем индикатор набора
        await message.bot.send_chat_action(message.chat.id, "typing")
        
        # Получаем ответ от Дикси
        response = await ask_dixi(message.text)
        
        # Отправляем ответ пользователю
        await message.answer(f"🤖 Дикси:\n\n{response}", reply_markup=get_menu_keyboard())
    else:
        # Игнорируем другие сообщения
        pass
