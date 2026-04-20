from aiogram import Router, types
from aiogram.filters import Command
from datetime import datetime
import re
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from app.services.openrouter_client import OpenRouterClient
from app.services.message_history import ChatMessage, get_message_history_service

router = Router()

# Создаем клавиатуру с кнопками меню
def get_menu_keyboard():
    builder = ReplyKeyboardBuilder()
    builder.button(text="🕒 Время")
    builder.button(text="📅 Дата")
    builder.button(text="ℹ️ Помощь")
    builder.button(text="🔍 DeepSeek")
    builder.button(text="🤖 Claude Haiku")
    builder.button(text="📋 Суммаризация чата")
    builder.button(text="🏠 Главное меню")
    builder.adjust(2, 2, 2, 1)  # 2 кнопки в первых трех рядах, 1 в последнем
    return builder.as_markup(resize_keyboard=True)

async def save_message_to_history(message: types.Message, is_bot: bool = False):
    """Сохраняет сообщение в историю"""
    try:
        history_service = get_message_history_service()
        
        chat_message = ChatMessage(
            chat_id=message.chat.id,
            user_id=message.from_user.id,
            username=message.from_user.username or message.from_user.first_name,
            message_text=message.text or message.caption or "[медиа-сообщение]",
            is_bot=is_bot,
            timestamp=datetime.now()
        )
        
        history_service.save_message(chat_message)
        return True
    except Exception as e:
        print(f"Error saving message to history: {e}")
        return False

@router.message(Command("help"))
async def cmd_help(message: types.Message):
    """Обработчик команды /help"""
    await save_message_to_history(message)
    help_text = (
        "🤖 Доступные команды:\n\n"
        "/start - Начать работу с ботом\n"
        "/help - Показать это сообщение\n"
        "/time - Показать текущее время\n"
        "/date - Показать текущую дату\n"
        "/deepseek - Задать вопрос DeepSeek модели\n"
        "/claude - Задать вопрос Claude Haiku модели\n"
        "/summarize - Суммаризировать последние 420 сообщений чата\n"
        "/history_stats - Показать статистику истории сообщений\n"
        "/menu - Показать меню с кнопками\n"
        "# Добавьте другие команды по необходимости"
    )
    await message.answer(help_text, reply_markup=get_menu_keyboard())
    await save_message_to_history(message, is_bot=True)

@router.message(Command("start"))
async def cmd_start(message: types.Message):
    """Обработчик команды /start"""
    await save_message_to_history(message)
    welcome_text = (
        "👋 Добро пожаловать!\n\n"
        "Я бот для работы с AI/LLM моделями.\n"
        "Используйте кнопки ниже или команды для навигации.\n\n"
        "Теперь доступны:\n"
        "• DeepSeek - мощная модель для сложных задач!\n"
        "• Claude Haiku - быстрая и умная модель от Anthropic!\n"
        "• Суммаризация чата - анализ последних 420 сообщений!\n"
        "• История сообщений - сохраняю все сообщения для контекста!\n\n"
        "Используйте команды /deepseek, /claude или /summarize"
    )
    await message.answer(welcome_text, reply_markup=get_menu_keyboard())
    await save_message_to_history(message, is_bot=True)

@router.message(Command("time"))
async def cmd_time(message: types.Message):
    """Обработчик команды /time - показывает текущее время"""
    await save_message_to_history(message)
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
    await save_message_to_history(message, is_bot=True)

@router.message(Command("date"))
async def cmd_date(message: types.Message):
    """Обработчик команды /date - показывает текущую дату"""
    await save_message_to_history(message)
    now = datetime.now()
    
    # Форматируем дату в читаемый вид
    months = [
        'января', 'февраля', 'марта', 'апреля', 'мая', 'июня',
        'июля', 'августа', 'сентября', 'октября', 'ноября', 'декабря'
    ]
    
    day = now.day
    month_name = months[now.month - 1]
    year = now.year
    
    date_text = (
        f"📅 Сегодня: {day} {month_name} {year} года"
    )
    await message.answer(date_text, reply_markup=get_menu_keyboard())
    await save_message_to_history(message, is_bot=True)

@router.message(Command("menu"))
async def cmd_menu(message: types.Message):
    """Обработчик команды /menu - показывает меню с кнопками"""
    await save_message_to_history(message)
    menu_text = "📱 Выберите действие из меню ниже:"
    await message.answer(menu_text, reply_markup=get_menu_keyboard())
    await save_message_to_history(message, is_bot=True)

@router.message(Command("deepseek"))
async def cmd_deepseek(message: types.Message):
    """Обработчик команды /deepseek - начинает работу с DeepSeek"""
    await save_message_to_history(message)
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
    await save_message_to_history(message, is_bot=True)

@router.message(Command("claude"))
async def cmd_claude(message: types.Message):
    """Обработчик команды /claude - начинает работу с Claude Haiku"""
    await save_message_to_history(message)
    instruction_text = (
        "🤖 Claude Haiku готов к работе!\n\n"
        "Отправьте мне любой запрос, и я передам его модели Claude Haiku через OpenRouter.\n\n"
        "Claude Haiku отлично справляется с:\n"
        "• Быстрыми и точными ответами\n"
        "• Общими вопросами и консультациями\n"
        "• Креативными задачами\n"
        "• Анализом текста и данных\n\n"
        "Задайте ваш вопрос..."
    )
    await message.answer(instruction_text, reply_markup=get_menu_keyboard())
    await save_message_to_history(message, is_bot=True)

@router.message(Command("history_stats"))
async def cmd_history_stats(message: types.Message):
    """Обработчик команды /history_stats - показывает статистику истории"""
    await save_message_to_history(message)
    try:
        history_service = get_message_history_service()
        message_count = history_service.get_message_count(message.chat.id)
        
        stats_text = (
            f"📊 Статистика истории сообщений:\n\n"
            f"• ID чата: {message.chat.id}\n"
            f"• Сохранено сообщений: {message_count}\n"
            f"• Для суммаризации доступно: {min(message_count, 420)} из 420\n\n"
            f"Используйте команду /summarize для анализа последних сообщений."
        )
        await message.answer(stats_text, reply_markup=get_menu_keyboard())
        await save_message_to_history(message, is_bot=True)
    except Exception as e:
        await message.answer(f"❌ Ошибка при получении статистики: {str(e)}", reply_markup=get_menu_keyboard())
        await save_message_to_history(message, is_bot=True)

@router.message(Command("summarize"))
async def cmd_summarize(message: types.Message):
    """Обработчик команды /summarize - суммаризирует последние 420 сообщений"""
    await save_message_to_history(message)
    try:
        # Отправляем сообщение о начале обработки
        await message.answer("📊 Начинаю суммаризацию последних 420 сообщений чата...", reply_markup=get_menu_keyboard())
        await save_message_to_history(message, is_bot=True)
        
        # Получаем историю сообщений из базы данных
        history_service = get_message_history_service()
        chat_history = history_service.get_recent_messages(message.chat.id, limit=420)
        
        if not chat_history:
            await message.answer("📭 История сообщений пуста. Начните общение с ботом!", reply_markup=get_menu_keyboard())
            await save_message_to_history(message, is_bot=True)
            return
        
        # Форматируем историю для отправки в модель
        formatted_history = []
        for msg in chat_history:
            sender = "🤖 Бот" if msg.is_bot else f"👤 {msg.username}"
            formatted_history.append(f"{sender}: {msg.message_text}")
        
        combined_history = "\n".join(formatted_history)
        
        # Если история слишком длинная, обрезаем ее
        if len(combined_history) > 8000:
            combined_history = combined_history[:8000] + "... [сообщение обрезано]"
        
        # Инициализируем клиент OpenRouter
        client = OpenRouterClient()
        
        # Отправляем запрос на суммаризацию в DeepSeek
        response = await client.chat_completion(
            messages=[
                {
                    "role": "system",
                    "content": (
                        "Ты - DeepSeek, мощная AI модель. Твоя задача - проанализировать историю чата "
                        "и создать краткую, информативную суммаризацию на русском языке. "
                        "Выдели основные темы, ключевые моменты, важные решения или обсуждения. "
                        "Будь точным и объективным. Предоставь суммаризацию в виде структурированного текста."
                    )
                },
                {
                    "role": "user",
                    "content": (
                        f"Пожалуйста, проанализируй следующую историю чата (последние {len(chat_history)} сообщений) "
                        f"и создай краткую суммаризацию:\n\n{combined_history}"
                    )
                }
            ],
            model="deepseek/deepseek-chat"
        )
        
        if response:
            summary_text = (
                f"📋 Суммаризация последних {len(chat_history)} сообщений чата:\n\n"
                f"{response}\n\n"
                f"---\n"
                f"🤖 Суммаризация выполнена с помощью DeepSeek через OpenRouter"
            )
            await message.answer(summary_text, reply_markup=get_menu_keyboard())
            await save_message_to_history(message, is_bot=True)
        else:
            await message.answer("⚠️ Не удалось получить суммаризацию. Попробуйте позже.", reply_markup=get_menu_keyboard())
            await save_message_to_history(message, is_bot=True)
    
    except Exception as e:
        await message.answer(f"❌ Ошибка при суммаризации чата: {str(e)}", reply_markup=get_menu_keyboard())
        await save_message_to_history(message, is_bot=True)

@router.message(lambda message: message.text in ["🕒 Время", "📅 Дата", "ℹ️ Помощь", "🔍 DeepSeek", "🤖 Claude Haiku", "📋 Суммаризация чата", "🏠 Главное меню"])
async def handle_menu_buttons(message: types.Message):
    """Обработчик нажатий на кнопки меню"""
    await save_message_to_history(message)
    if message.text == "🕒 Время":
        await cmd_time(message)
    elif message.text == "📅 Дата":
        await cmd_date(message)
    elif message.text == "ℹ️ Помощь":
        await cmd_help(message)
    elif message.text == "🔍 DeepSeek":
        await cmd_deepseek(message)
    elif message.text == "🤖 Claude Haiku":
        await cmd_claude(message)
    elif message.text == "📋 Суммаризация чата":
        await cmd_summarize(message)
    elif message.text == "🏠 Главное меню":
        await cmd_menu(message)

@router.message()
async def process_other_messages(message: types.Message):
    """Обработчик всех остальных сообщений"""
    # Сохраняем сообщение пользователя в историю
    await save_message_to_history(message)
    
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
            await save_message_to_history(message, is_bot=True)
        else:
            await message.answer("⚠️ Извините, DeepSeek временно недоступен. Попробуйте позже.", reply_markup=get_menu_keyboard())
            await save_message_to_history(message, is_bot=True)
    
    except Exception as e:
        await message.answer(f"❌ Ошибка при обращении к DeepSeek: {str(e)}", reply_markup=get_menu_keyboard())
        await save_message_to_history(message, is_bot=True)

@router.message(lambda message: message.text and message.text.startswith("/deepseek_"))
async def process_deepseek_query(message: types.Message):
    """Обработчик прямых запросов к DeepSeek через команду"""
    await save_message_to_history(message)
    query = message.text.replace("/deepseek_", "", 1).strip()
    if not query:
        await message.answer("🔍 Пожалуйста, укажите запрос после команды /deepseek_")
        await save_message_to_history(message, is_bot=True)
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
            await save_message_to_history(message, is_bot=True)
        else:
            await message.answer("⚠️ Извините, DeepSeek временно недоступен. Попробуйте позже.", reply_markup=get_menu_keyboard())
            await save_message_to_history(message, is_bot=True)
    
    except Exception as e:
        await message.answer(f"❌ Ошибка при обращении к DeepSeek: {str(e)}", reply_markup=get_menu_keyboard())
        await save_message_to_history(message, is_bot=True)

@router.message(lambda message: message.text and message.text.startswith("/claude_"))
async def process_claude_query(message: types.Message):
    """Обработчик прямых запросов к Claude Haiku через команду"""
    await save_message_to_history(message)
    query = message.text.replace("/claude_", "", 1).strip()
    if not query:
        await message.answer("🤖 Пожалуйста, укажите запрос после команды /claude_")
        await save_message_to_history(message, is_bot=True)
        return
    
    try:
        client = OpenRouterClient()
        
        # Используем модель Claude Haiku через OpenRouter
        response = await client.chat_completion(
            messages=[
                {
                    "role": "system",
                    "content": "Ты - Claude Haiku, быстрая и умная AI модель от Anthropic. Отвечай на русском языке, будь точным, креативным и полезным."
                },
                {
                    "role": "user",
                    "content": query
                }
            ],
            model="anthropic/claude-3-haiku"  # Указываем модель Claude Haiku
        )
        
        if response:
            await message.answer(f"🤖 Claude Haiku: {response}", reply_markup=get_menu_keyboard())
            await save_message_to_history(message, is_bot=True)
        else:
            await message.answer("⚠️ Извините, Claude Haiku временно недоступен. Попробуйте позже.", reply_markup=get_menu_keyboard())
            await save_message_to_history(message, is_bot=True)
    
    except Exception as e:
        await message.answer(f"❌ Ошибка при обращении к Claude Haiku: {str(e)}", reply_markup=get_menu_keyboard())
        await save_message_to_history(message, is_bot=True)