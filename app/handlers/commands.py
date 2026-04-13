from aiogram import Router, types
from aiogram.filters import Command
from datetime import datetime
import re
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
import config
from app.utils.openrouter import get_available_models, send_message_to_openrouter

router = Router()

# Состояния для FSM
class DixiStates(StatesGroup):
    waiting_for_message = State()

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
        "/menu - Показать меню с кнопками\n"
        "/dixi - Начать диалог с AI ассистентом\n"
        "/models - Показать доступные модели LLM"
    )
    await message.answer(help_text, reply_markup=get_menu_keyboard())

@router.message(Command("start"))
async def cmd_start(message: types.Message):
    """Обработчик команды /start"""
    welcome_text = (
        "👋 Добро пожаловать!\n\n"
        "Я бот для работы с AI/LLM моделями.\n"
        "Используйте кнопки ниже или команды для навигации.\n\n"
        "Новая функция: Дикси 🤖 - AI ассистент через OpenRouter\n"
        "Используйте /dixi чтобы начать общение"
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
async def cmd_dixi(message: types.Message, state: FSMContext):
    """Обработчик команды /dixi - начинает диалог с AI ассистентом"""
    if not config.OPENROUTER_API_KEY:
        await message.answer("❌ Ключ OpenRouter не настроен. Обратитесь к администратору.")
        return
    
    await message.answer(
        "🤖 Дикси готов к общению!\n"
        "Напишите ваш вопрос или сообщение.\n"
        "Для выхода из режима диалога отправьте /cancel"
    )
    await state.set_state(DixiStates.waiting_for_message)

@router.message(Command("models"))
async def cmd_models(message: types.Message):
    """Обработчик команды /models - показывает доступные модели LLM"""
    if not config.OPENROUTER_API_KEY:
        await message.answer("❌ Ключ OpenRouter не настроен. Обратитесь к администратору.")
        return
    
    await message.answer("🔄 Загружаю список доступных моделей...")
    
    try:
        models = await get_available_models()
        if models:
            models_text = "📋 Доступные модели LLM:\n\n"
            for model in models[:10]:  # Показываем первые 10 моделей
                models_text += f"• {model.get('id', 'N/A')}\n"
                if model.get('description'):
                    models_text += f"  {model['description'][:50]}...\n"
                models_text += "\n"
            
            if len(models) > 10:
                models_text += f"... и еще {len(models) - 10} моделей"
            
            await message.answer(models_text)
        else:
            await message.answer("❌ Не удалось загрузить список моделей")
    except Exception as e:
        await message.answer(f"❌ Ошибка при загрузке моделей: {str(e)}")

@router.message(Command("cancel"))
async def cmd_cancel(message: types.Message, state: FSMContext):
    """Обработчик команды /cancel - отмена текущего действия"""
    current_state = await state.get_state()
    if current_state is None:
        return
    
    await state.clear()
    await message.answer("✅ Диалог завершен", reply_markup=get_menu_keyboard())

@router.message(DixiStates.waiting_for_message)
async def process_dixi_message(message: types.Message, state: FSMContext):
    """Обработчик сообщений в режиме диалога с Дикси"""
    if not config.OPENROUTER_API_KEY:
        await message.answer("❌ Ключ OpenRouter не настроен.")
        await state.clear()
        return
    
    user_message = message.text
    
    if not user_message or user_message.strip() == "":
        await message.answer("Пожалуйста, введите текст сообщения")
        return
    
    # Показываем индикатор набора
    typing_message = await message.answer("✍️ Дикси думает...")
    
    try:
        response = await send_message_to_openrouter(user_message)
        
        # Удаляем индикатор набора
        await typing_message.delete()
        
        if response:
            await message.answer(f"🤖 Дикси:\n\n{response}")
        else:
            await message.answer("❌ Не удалось получить ответ от AI")
    except Exception as e:
        # Удаляем индикатор набора
        await typing_message.delete()
        await message.answer(f"❌ Ошибка: {str(e)}")
    
    # Остаемся в том же состоянии для продолжения диалога
    await state.set_state(DixiStates.waiting_for_message)

@router.message(lambda message: message.text in ["🕒 Время", "ℹ️ Помощь", "🤖 Дикси", "🏠 Главное меню"])
async def handle_menu_buttons(message: types.Message, state: FSMContext):
    """Обработчик нажатий на кнопки меню"""
    if message.text == "🕒 Время":
        await cmd_time(message)
    elif message.text == "ℹ️ Помощь":
        await cmd_help(message)
    elif message.text == "🤖 Дикси":
        await cmd_dixi(message, state)
    elif message.text == "🏠 Главное меню":
        current_state = await state.get_state()
        if current_state:
            await state.clear()
        await cmd_menu(message)

@router.message()
async def process_other_messages(message: types.Message):
    """Обработчик всех остальных сообщений"""
    # Игнорируем сообщения, которые не являются командами или кнопками меню
    pass
