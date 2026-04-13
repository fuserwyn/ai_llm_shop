from aiogram import Router, types
from aiogram.filters import Command
from datetime import datetime
import re
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from app.services.openrouter_client import OpenRouterClient

router = Router()

# Глобальная переменная для отслеживания активного режима
active_mode = {}

# Создаем клавиатуру с кнопками меню
def get_menu_keyboard():
    builder = ReplyKeyboardBuilder()
    builder.button(text="🕒 Время")
    builder.button(text="ℹ️ Помощь")
    builder.button(text="🤖 Дикси")
    builder.button(text="🔍 DeepSeek")
    builder.button(text="🏠 Главное меню")
    builder.adjust(2, 2, 1)  # 2 кнопки в первых двух рядах, 1 в последнем
    return builder.as_markup(resize_keyboard=True)

@router.message(Command("help"))
async def cmd_help(message: types.Message):
    """Обработчик команды /help"""
    help_text = (
        "🤖 Доступные команды:\n\n"
        "/start - Начать работу с ботом\n"
        "/help - Показать это сообщение\n"
        "/time - Показать текущее время\n"
        "/dixi - Поговорить с Дикси (AI ассистент)\n"
        "/deepseek - Поговорить с DeepSeek (продвинутый AI)\n"
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
        "• Дикси - AI ассистент через OpenRouter!\n"
        "• DeepSeek - продвинутый AI модель через OpenRouter!\n\n"
        "Используйте команды /dixi или /deepseek или соответствующие кнопки"
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
    # Устанавливаем режим Дикси для пользователя
    active_mode[message.from_user.id] = "dixi"
    
    instruction_text = (
        "🤖 Дикси готов к общению!\n\n"
        "Отправьте мне любое сообщение, и я передам его Дикси - вашему AI ассистенту через OpenRouter.\n\n"
        "Дикси может:\n"
        "• Отвечать на вопросы\n"
        "• Помогать с кодом\n"
        "• Обсуждать идеи\n"
        "• И многое другое!\n\n"
        "Просто напишите что-нибудь..."
    )
    await message.answer(instruction_text, reply_markup=get_menu_keyboard())

@router.message(Command("deepseek"))
async def cmd_deepseek(message: types.Message):
    """Обработчик команды /deepseek - начинает диалог с DeepSeek"""
    # Устанавливаем режим DeepSeek для пользователя
    active_mode[message.from_user.id] = "deepseek"
    
    instruction_text = (
        "🔍 DeepSeek готов к общению!\n\n"
        "Отправьте мне любое сообщение, и я передам его DeepSeek - продвинутой AI модели через OpenRouter.\n\n"
        "DeepSeek может:\n"
        "• Решать сложные задачи\n"
        "• Анализировать код\n"
        "• Помогать с исследованиями\n"
        "• Обсуждать технические темы\n"
        "• И многое другое!\n\n"
        "Просто напишите что-нибудь..."
    )
    await message.answer(instruction_text, reply_markup=get_menu_keyboard())

@router.message(lambda message: message.text in ["🕒 Время", "ℹ️ Помощь", "🤖 Дикси", "🔍 DeepSeek", "🏠 Главное меню"])
async def handle_menu_buttons(message: types.Message):
    """Обработчик нажатий на кнопки меню"""
    if message.text == "🕒 Время":
        await cmd_time(message)
    elif message.text == "ℹ️ Помощь":
        await cmd_help(message)
    elif message.text == "🤖 Дикси":
        await cmd_dixi(message)
    elif message.text == "🔍 DeepSeek":
        await cmd_deepseek(message)
    elif message.text == "🏠 Главное меню":
        await cmd_menu(message)

@router.message()
async def process_other_messages(message: types.Message):
    """Обработчик всех остальных сообщений"""
    user_id = message.from_user.id
    
    # Определяем, какой режим использовать
    # Если пользователь недавно вызывал /deepseek, используем DeepSeek
    # Иначе используем Дикси
    use_deepseek = active_mode.get(user_id) == "deepseek"
    
    # Сбрасываем режим после использования
    if user_id in active_mode:
        del active_mode[user_id]
    
    try:
        # Инициализируем клиент OpenRouter
        client = OpenRouterClient()
        
        if use_deepseek:
            # Используем DeepSeek модель
            model = "deepseek/deepseek-chat"
            system_prompt = "Ты - DeepSeek, продвинутый AI ассистент. Отвечай на русском языке, будь точным, информативным и полезным. Ты специализируешься на технических и сложных вопросах."
            assistant_name = "DeepSeek"
        else:
            # Используем стандартную модель (Дикси)
            model = None  # Будет использована модель из конфигурации
            system_prompt = "Ты - Дикси, дружелюбный AI ассистент. Отвечай на русском языке, будь полезным и вежливым."
            assistant_name = "Дикси"
        
        # Отправляем сообщение пользователя в OpenRouter
        response = await client.chat_completion(
            messages=[
                {
                    "role": "system",
                    "content": system_prompt
                },
                {
                    "role": "user",
                    "content": message.text
                }
            ],
            model=model
        )
        
        if response:
            await message.answer(f"🤖 {assistant_name}: {response}", reply_markup=get_menu_keyboard())
        else:
            await message.answer(f"⚠️ Извините, {assistant_name} временно недоступен. Попробуйте позже.", reply_markup=get_menu_keyboard())
    
    except Exception as e:
        await message.answer(f"❌ Ошибка при обращении к AI: {str(e)}", reply_markup=get_menu_keyboard())
