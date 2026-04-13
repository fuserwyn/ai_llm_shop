from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters.callback_data import CallbackData
from app.handlers.commands import MenuCallback

def main_menu_keyboard() -> InlineKeyboardMarkup:
    """Создает основную клавиатуру меню"""
    buttons = [
        [
            InlineKeyboardButton(text="🕒 Текущее время", callback_data=MenuCallback(action="time").pack()),
            InlineKeyboardButton(text="❓ Помощь", callback_data=MenuCallback(action="help").pack())
        ],
        [
            InlineKeyboardButton(text="📋 Главное меню", callback_data=MenuCallback(action="main_menu").pack())
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)

def help_keyboard() -> InlineKeyboardMarkup:
    """Создает клавиатуру для раздела помощи"""
    buttons = [
        [
            InlineKeyboardButton(text="🕒 Текущее время", callback_data=MenuCallback(action="time").pack()),
            InlineKeyboardButton(text="🏠 Главное меню", callback_data=MenuCallback(action="main_menu").pack())
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)
