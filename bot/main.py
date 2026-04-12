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
        "Я могу:\n"
        "- Показать текущее время и дату (/time, /date)\n"
        "- Ответить на ваши вопросы (просто напишите что-нибудь)\n"
        "- Помочь с помощью (/help)"
    )


@dp.message(Command("help"))
async def help_command(message: Message):
    await message.answer(
        "Доступные команды:\n"
        "/start - Начало работы\n"
        "/help - Эта справка\n"
        "/time - Текущее время\n"
        "/date - Текущая дата\n"
        "\n"
        "Вы также можете просто написать мне вопрос, и я постараюсь ответить с помощью AI."
    )


@dp.message(Command("time"))
async def time_command(message: Message):
    current_time = datetime.now().strftime("%H:%M:%S")
    await message.answer(f"Текущее время: {current_time}")


@dp.message(Command("date"))
async def date_command(message: Message):
    current_date = datetime.now().strftime("%d.%m.%Y")
    await message.answer(f"Текущая дата: {current_date}")


async def get_ai_response(user_message: str) -> Optional[str]:
    """Получить ответ от OpenRouter AI"""
    if not OPENROUTER_API_KEY:
        return None

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
    }

    payload = {
        "model": "openai/gpt-3.5-turbo",
        "messages": [
            {
                "role": "system",
                "content": "Ты полезный помощник в Telegram боте. Отвечай кратко и по делу."
            },
            {"role": "user", "content": user_message}
        ],
        "max_tokens": 500,
    }

    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(
                OPENROUTER_URL, headers=headers, json=payload, timeout=30
            ) as response:
                if response.status == 200:
                    data = await response.json()
                    return data["choices"][0]["message"]["content"]
                else:
                    return None
    except Exception:
        return None


@dp.message()
async def handle_message(message: Message):
    """Обработка всех остальных сообщений через AI"""
    if message.text.startswith("/"):
        await message.answer("Неизвестная команда. Используйте /help для списка команд.")
        return

    await message.answer("Думаю...")
    ai_response = await get_ai_response(message.text)

    if ai_response:
        await message.answer(ai_response)
    else:
        await message.answer(
            "Извините, не могу получить ответ от AI. "
            "Проверьте настройки API или попробуйте позже."
        )


async def main():
    print("Бот запущен!")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
