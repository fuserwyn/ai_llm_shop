import asyncio
from datetime import datetime
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.enums import ParseMode

API_TOKEN = "YOUR_BOT_TOKEN_HERE"  # Replace with your actual token

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer(
        "👋 Hello! I'm your assistant bot.\n"
        "I can help you with:\n"
        "• /date - show current date\n"
        "• /time - show current time\n"
        "• /help - list all commands"
    )

@dp.message(Command("help"))
async def cmd_help(message: types.Message):
    await message.answer(
        "Available commands:\n"
        "/start - Welcome message\n"
        "/help - This help list\n"
        "/date - Current date\n"
        "/time - Current time"
    )

@dp.message(Command("date"))
async def cmd_date(message: types.Message):
    now = datetime.now()
    date_str = now.strftime("%A, %B %d, %Y")
    await message.answer(f"📅 Today's date: {date_str}")

@dp.message(Command("time"))
async def cmd_time(message: types.Message):
    now = datetime.now()
    time_str = now.strftime("%H:%M:%S")
    await message.answer(f"🕒 Current time: {time_str}")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
