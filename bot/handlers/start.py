from aiogram import Router, types
from aiogram.filters import Command
from aiogram.utils.keyboard import ReplyKeyboardBuilder

router = Router()

@router.message(Command("start"))
async def cmd_start(message: types.Message):
    builder = ReplyKeyboardBuilder()
    builder.add(
        types.KeyboardButton(text="🛒 Каталог"),
        types.KeyboardButton(text="🛒 Корзина"),
        types.KeyboardButton(text="📦 Мои заказы"),
        types.KeyboardButton(text="ℹ️ Помощь"),
        types.KeyboardButton(text="⚙️ Настройки")
    )
    builder.adjust(2, 2, 1)
    keyboard = builder.as_markup(resize_keyboard=True)
    await message.answer(
        "Добро пожаловать в магазин! Выберите действие:",
        reply_markup=keyboard
    )