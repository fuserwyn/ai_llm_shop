from aiogram import Router, types
from aiogram.filters import Command
from aiogram.utils.keyboard import ReplyKeyboardBuilder

router = Router()

@router.message(Command("help"))
async def cmd_help(message: types.Message):
    builder = ReplyKeyboardBuilder()
    builder.add(
        types.KeyboardButton(text="/start"),
        types.KeyboardButton(text="/shop"),
        types.KeyboardButton(text="/cart")
    )
    builder.adjust(2)
    await message.answer(
        "Доступные команды:\n"
        "/start - начать работу\n"
        "/shop - просмотр товаров\n"
        "/cart - корзина\n\n"
        "Используй кнопки для удобства!",
        reply_markup=builder.as_markup(resize_keyboard=True)
    )
