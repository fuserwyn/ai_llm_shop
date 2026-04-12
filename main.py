import os
from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message
import asyncio
from config import TELEGRAM_BOT_TOKEN, OPENROUTER_API_KEY, OPENROUTER_MODEL

bot = Bot(token=TELEGRAM_BOT_TOKEN)
dp = Dispatcher()

@dp.message(Command('start'))
async def start_command(message: Message):
    await message.answer('Hello! I am your AI assistant bot.')

async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())