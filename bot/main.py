import asyncio
import os
from datetime import datetime
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import Message
from openai import AsyncOpenAI
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"

bot = Bot(token=TOKEN)
dp = Dispatcher()
client = AsyncOpenAI(
    api_key=OPENROUTER_API_KEY,
    base_url=OPENROUTER_BASE_URL,
)

@dp.message(Command("start"))
async def start_command(message: Message):
    await message.answer("Привет! Я ваш помощник. Используйте /help для списка команд.")

@dp.message(Command("help"))
async def help_command(message: Message):
    help_text = (
        "Доступные команды:\n"
        "/start - Начать работу\n"
        "/help - Показать это сообщение\n"
        "/time - Текущее время\n"
        "/date - Текущая дата\n"
        "Или просто напишите мне вопрос, и я постараюсь ответить!"
    )
    await message.answer(help_text)

@dp.message(Command("time"))
async def time_command(message: Message):
    current_time = datetime.now().strftime("%H:%M:%S")
    await message.answer(f"Текущее время: {current_time}")

@dp.message(Command("date"))
async def date_command(message: Message):
    current_date = datetime.now().strftime("%d.%m.%Y")
    await message.answer(f"Текущая дата: {current_date}")

@dp.message()
async def handle_message(message: Message):
    user_input = message.text.strip()
    if not user_input:
        return
    
    try:
        response = await client.chat.completions.create(
            model="openai/gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": user_input}
            ],
            max_tokens=500,
        )
        answer = response.choices[0].message.content
        await message.answer(answer)
    except Exception as e:
        await message.answer(f"Извините, произошла ошибка: {str(e)}")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
