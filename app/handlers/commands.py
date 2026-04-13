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
    builder.button(text="🤖 Дикси")
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
        "/dixi - Поговорить с Дикси (AI ассистент)\n"
        "/menu - Показать меню с кнопками\n\n"
        "🤖 Дикси работает через OpenRouter API. После команды /dixi просто отправляйте сообщения - они будут переданы AI ассистенту."
    )
    await message.answer(help_text, reply_markup=get_menu_keyboard())

@router.message(Command("start"))
async def cmd_start(message: types.Message):
    """Обработчик команды /start"""
    welcome_text = (
        "👋 Добро пожаловать!\n\n"
        "Я бот для работы с AI/LLM моделями.\n"
        "Используйте кнопки ниже или команды для навигации.\n\n"
        "Теперь доступен Дикси - AI ассистент через OpenRouter!\n"
        "Используйте команду /dixi или кнопку '🤖 Дикси'\n\n"
        "Для работы Дикси необходим API ключ OpenRouter.\n"
        "Получите его на https://openrouter.ai и добавьте в .env файл."
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
    instruction_text = (
        "🤖 Дикси готов к общению!\n\n"
        "Отправьте мне любое сообщение, и я передам его Дикси - вашему AI ассистенту через OpenRouter.\n\n"
        "Дикси может:\n"
        "• Отвечать на вопросы\n"
        "• Помогать с кодом\n"
        "• Обсуждать идеи\n"
        "• И многое другое!\n\n"
        "Просто напишите что-нибудь...\n\n"
        "⚠️ Для работы необходим API ключ OpenRouter в .env файле."
    )
    await message.answer(instruction_text, reply_markup=get_menu_keyboard())

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

# Глобальный флаг для отслеживания режима Дикси
dixi_mode_users = set()

@router.message()
async def process_other_messages(message: types.Message):
    """Обработчик всех остальных сообщений"""
    # Проверяем, находится ли пользователь в режиме Дикси
    # (после команды /dixi или нажатия кнопки Дикси)
    user_id = message.from_user.id
    
    # Если пользователь отправил /dixi или нажал кнопку Дикси, включаем режим
    if message.text == "/dixi" or message.text == "🤖 Дикси":
        dixi_mode_users.add(user_id)
        return
    
    # Если пользователь в режиме Дикси, обрабатываем сообщение через OpenRouter
    if user_id in dixi_mode_users:
        try:
            # Инициализируем клиент OpenRouter
            client = OpenRouterClient()
            
            # Отправляем сообщение пользователя в OpenRouter
            response = await client.chat_completion(
                messages=[
                    {
                        "role": "system",
                        "content": "Ты - Дикси, дружелюбный AI ассистент. Отвечай на русском языке, будь полезным и вежливым. Отвечай кратко и по делу."
                    },
                    {
                        "role": "user",
                        "content": message.text
                    }
                ]
            )
            
            if response:
                await message.answer(f"🤖 Дикси: {response}", reply_markup=get_menu_keyboard())
            else:
                await message.answer("⚠️ Извините, Дикси временно недоступен. Попробуйте позже.", reply_markup=get_menu_keyboard())
        
        except ValueError as e:
            if "OPENROUTER_API_KEY не установлен" in str(e):
                await message.answer(
                    "❌ API ключ OpenRouter не настроен.\n\n"
                    "Для работы Дикси необходимо:\n"
                    "1. Получить API ключ на https://openrouter.ai\n"
                    "2. Добавить его в .env файл:\n"
                    "   OPENROUTER_API_KEY=ваш_ключ\n\n"
                    "После настройки перезапустите бота.",
                    reply_markup=get_menu_keyboard()
                )
                # Выключаем режим Дикси для этого пользователя
                dixi_mode_users.discard(user_id)
            else:
                await message.answer(f"❌ Ошибка: {str(e)}", reply_markup=get_menu_keyboard())
        
        except Exception as e:
            await message.answer(f"❌ Ошибка при обращении к Дикси: {str(e)}", reply_markup=get_menu_keyboard())
    else:
        # Если не в режиме Дикси, просто показываем меню
        await message.answer("Выберите действие из меню ниже или используйте команду /dixi для общения с AI ассистентом.", reply_markup=get_menu_keyboard())

# Обработчик для сброса режима Дикси при других командах
@router.message(Command("start", "help", "time", "menu"))
async def reset_dixi_mode(message: types.Message):
    """Сбрасывает режим Дикси при использовании других команд"""
    dixi_mode_users.discard(message.from_user.id)