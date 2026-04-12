import asyncio
import os
from datetime import datetime
from typing import Optional

import aiohttp
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import Message
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"

bot = Bot(token=TOKEN)
dp = Dispatcher()


@dp.message(Command("start"))
async def start_command(message: Message):
    await message.answer(
        "Привет! Я ваш помощник.\n"
        "Доступные команды:\n"
        "/time - текущее время\n"
        "/date - текущая дата\n"
        "/help - справка\n"
        "Или просто напишите вопрос, и я постараюсь помочь!"
    )


@dp.message(Command("help"))
async def help_command(message: Message):
    await message.answer(
        "Я могу:\n"
        "• Показать текущее время (/time)\n"
        "• Показать текущую дату (/date)\n"
        "• Ответить на ваши вопросы с помощью AI\n"
        "Просто напишите мне что-нибудь!"
    )


@dp.message(Command("time"))
async def time_command(message: Message):
    current_time = datetime.now().strftime("%H:%M:%S")
    await message.answer(f"Текущее время: {current_time}")


@dp.message(Command("date"))
async def date_command(message: Message):
    current_date = datetime.now().strftime("%d.%m.%Y")
    await message.answer(f"Текущая дата: {current_date}")


async def get_ai_response(prompt: str) -> Optional[str]:
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": "openai/gpt-3.5-turbo",
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 500,
    }

    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(
                OPENROUTER_URL, headers=headers, json=payload
            ) as response:
                if response.status == 200:
                    data = await response.json()
                    return data["choices"][0]["message"]["content"].strip()
                else:
                    return f"Ошибка API: {response.status}"
    except Exception as e:
        return f"Ошибка соединения: {e}"


@dp.message()
async def handle_message(message: Message):
    if message.text.startswith("/"):
        return

    await message.answer("Думаю...")
    response = await get_ai_response(message.text)
    if response:
        await message.answer(response)
    else:
        await message.answer("Не удалось получить ответ от AI.")


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
