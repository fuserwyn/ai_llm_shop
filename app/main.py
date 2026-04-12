import logging
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties

from app.core.config import settings
from app.handlers import (
    start_handler,
    help_handler,
    # ... другие импорты ...
    deepseek_handler  # Добавляем импорт нового обработчика
)

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def main() -> None:
    # Инициализация бота
    bot = Bot(
        token=settings.BOT_TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )
    dp = Dispatcher()
    
    # Регистрация роутеров
    dp.include_router(start_handler.router)
    dp.include_router(help_handler.router)
    # ... другие роутеры ...
    dp.include_router(deepseek_handler.router)  # Регистрируем новый обработчик
    
    # Запуск бота
    await dp.start_polling(bot)


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())