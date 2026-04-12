from aiogram import Router, types
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

router = Router()

@router.message(Command("start"))
async def start_command(message: types.Message):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🛒 Товары", callback_data="products")],
        [InlineKeyboardButton(text="📦 Мои заказы", callback_data="orders")],
        [InlineKeyboardButton(text="💰 Баланс", callback_data="balance")],
        [InlineKeyboardButton(text="ℹ️ Помощь", callback_data="help")]
    ])
    await message.answer(
        "Добро пожаловать в магазин! Выберите действие:",
        reply_markup=keyboard
    )

@router.callback_query(lambda c: c.data == "products")
async def show_products(callback: types.CallbackQuery):
    await callback.message.edit_text("Список товаров будет здесь...")
    await callback.answer()

@router.callback_query(lambda c: c.data == "orders")
async def show_orders(callback: types.CallbackQuery):
    await callback.message.edit_text("Ваши заказы будут здесь...")
    await callback.answer()

@router.callback_query(lambda c: c.data == "balance")
async def show_balance(callback: types.CallbackQuery):
    await callback.message.edit_text("Ваш баланс будет здесь...")
    await callback.answer()

@router.callback_query(lambda c: c.data == "help")
async def show_help(callback: types.CallbackQuery):
    await callback.message.edit_text("Помощь будет здесь...")
    await callback.answer()