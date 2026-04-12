from aiogram import Router, types
from aiogram.filters import Command
from datetime import datetime

router = Router()

@router.message(Command("help"))
async def cmd_help(message: types.Message):
    """Обработчик команды /help"""
    help_text = (
        "🤖 Доступные команды:\n\n"
        "/start - Начать работу с ботом\n"
        "/help - Показать это сообщение\n"
        "/set_datetime - Установить дату и время\n"
        "# Добавьте другие команды по необходимости"
    )
    await message.answer(help_text)

@router.message(Command("start"))
async def cmd_start(message: types.Message):
    """Обработчик команды /start"""
    welcome_text = (
        "👋 Добро пожаловать!\n\n"
        "Я бот для работы с AI/LLM моделями.\n"
        "Используйте /help для списка команд."
    )
    await message.answer(welcome_text)

@router.message(Command("set_datetime"))
async def cmd_set_datetime(message: types.Message):
    """Обработчик команды /set_datetime"""
    args = message.text.split()[1:]  # Пропускаем саму команду
    
    if len(args) < 2:
        await message.answer(
            "❌ Неверный формат команды. Используйте:\n"
            "`/set_datetime [дата] [время]`\n\n"
            "Пример:\n"
            "`/set_datetime 2024-12-25 15:30:00`\n\n"
            "Формат даты: ГГГГ-ММ-ДД\n"
            "Формат времени: ЧЧ:ММ:СС"
        )
        return
    
    date_str = args[0]
    time_str = args[1]
    
    try:
        # Пробуем распарсить дату и время
        datetime_str = f"{date_str} {time_str}"
        dt = datetime.strptime(datetime_str, "%Y-%m-%d %H:%M:%S")
        
        # Здесь можно добавить логику сохранения даты (в БД, кэш и т.д.)
        # Например: await save_datetime(message.from_user.id, dt)
        
        await message.answer(
            f"✅ Дата и время установлены:\n"
            f"📅 {dt.strftime('%d.%m.%Y')} \n"
            f"⏰ {dt.strftime('%H:%M:%S')}\n\n"
            f"(ISO формат: {dt.isoformat()})"
        )
    except ValueError as e:
        await message.answer(
            f"❌ Ошибка парсинга даты/времени: {e}\n\n"
            "Проверьте формат:\n"
            "• Дата: ГГГГ-ММ-ДД (например: 2024-12-25)\n"
            "• Время: ЧЧ:ММ:СС (например: 15:30:00)"
        )