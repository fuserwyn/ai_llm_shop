from aiogram import Router, types
from aiogram.filters import Text

router = Router()

@router.message(Text("🛒 Каталог"))
async def catalog_menu(message: types.Message):
    await message.answer("Раздел каталога. Здесь будут товары.")

@router.message(Text("🛒 Корзина"))
async def cart_menu(message: types.Message):
    await message.answer("Ваша корзина. Тут будут товары в корзине.")

@router.message(Text("📦 Мои заказы"))
async def orders_menu(message: types.Message):
    await message.answer("История заказов. Тут будут ваши заказы.")

@router.message(Text("ℹ️ Помощь"))
async def help_menu(message: types.Message):
    await message.answer("Помощь по боту. Тут будет инструкция.")

@router.message(Text("⚙️ Настройки"))
async def settings_menu(message: types.Message):
    await message.answer("Настройки. Тут можно настроить бота.")