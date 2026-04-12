from aiogram import Router, types
from aiogram.filters import Command
from aiogram.utils.keyboard import ReplyKeyboardBuilder

router = Router()

@router.message(Command("start"))
async def cmd_start(message: types.Message):
    builder = ReplyKeyboardBuilder()
    builder.add(
        types.KeyboardButton(text="/help"),
        types.KeyboardButton(text="/shop"),
        types.KeyboardButton(text="/cart")
    )
    builder.adjust(2)
    await message.answer(
        "Привет! Я бот магазина. Используй кнопки ниже:",
        reply_markup=builder.as_markup(resize_keyboard=True)
    )
