from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message

router = Router()

@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer("Hello! Bot is working without database.")

@router.message()
async def echo(message: Message):
    await message.answer(f"Echo: {message.text}")