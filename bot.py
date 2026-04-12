import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
from aiohttp import web
import os
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize bot and dispatcher
bot = Bot(token=os.getenv('BOT_TOKEN'))
dp = Dispatcher()

# Command handlers
@dp.message(Command('start'))
async def cmd_start(message: Message):
    await message.answer("Привет! Я простой бот. Используй /help для списка команд.")

@dp.message(Command('help'))
async def cmd_help(message: Message):
    help_text = "Доступные команды:\n/start - Начать работу\n/help - Помощь\n/date - Текущая дата и время"
    await message.answer(help_text)

@dp.message(Command('date'))
async def cmd_date(message: Message):
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    await message.answer(f"Текущая дата и время: {current_time}")

# Webhook setup
async def on_startup(bot: Bot):
    webhook_url = os.getenv('WEBHOOK_URL')
    if webhook_url:
        await bot.set_webhook(webhook_url)
        logger.info(f"Webhook set to {webhook_url}")

async def on_shutdown(bot: Bot):
    logger.info("Shutting down...")
    await bot.session.close()

# Main function
def main():
    app = web.Application()
    webhook_requests_handler = SimpleRequestHandler(
        dispatcher=dp,
        bot=bot,
    )
    webhook_requests_handler.register(app, path="/webhook")
    setup_application(app, dp, bot=bot)
    app.on_startup.append(on_startup)
    app.on_shutdown.append(on_shutdown)
    web.run_app(app, host="0.0.0.0", port=8080)

if __name__ == "__main__":
    main()
