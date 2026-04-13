from aiogram import Router, types
from aiogram.filters import Command
import httpx
import config
from aiogram.utils.keyboard import ReplyKeyboardBuilder

router = Router()

# Создаем клавиатуру с кнопками меню
def get_menu_keyboard():
    builder = ReplyKeyboardBuilder()
    builder.button(text="🕒 Время")
    builder.button(text="ℹ️ Помощь")
    builder.button(text="🏠 Главное меню")
    builder.button(text="🤖 Dixi")
    builder.adjust(2, 2)  # 2 кнопки в первом ряду, 2 во втором
    return builder.as_markup(resize_keyboard=True)

@router.message(Command("dixi"))
async def cmd_dixi(message: types.Message):
    """Обработчик команды /dixi - отправляет сообщение в OpenRouter"""
    if not config.OPENROUTER_API_KEY:
        await message.answer("❌ Ключ OpenRouter не настроен. Добавьте OPENROUTER_API_KEY в .env файл.", reply_markup=get_menu_keyboard())
        return

    # Если команда без текста, просим ввести сообщение
    if not message.text or message.text.strip() == '/dixi':
        await message.answer("💬 Введите сообщение для Dixi после команды /dixi, например: /dixi Привет!", reply_markup=get_menu_keyboard())
        return

    # Извлекаем текст после команды
    user_text = message.text.strip().split('/dixi', 1)[1].strip()
    if not user_text:
        await message.answer("💬 Введите сообщение для Dixi после команды /dixi, например: /dixi Привет!", reply_markup=get_menu_keyboard())
        return

    try:
        # Запрос к OpenRouter API
        headers = {
            "Authorization": f"Bearer {config.OPENROUTER_API_KEY}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": "openrouter/auto",  # Автоматический выбор модели через OpenRouter
            "messages": [
                {"role": "user", "content": user_text}
            ],
            "max_tokens": 500
        }

        async with httpx.AsyncClient() as client:
            response = await client.post("https://openrouter.ai/api/v1/chat/completions", json=payload, headers=headers)
            if response.status_code == 200:
                data = response.json()
                reply = data["choices"][0]["message"]["content"]
                await message.answer(f"🤖 Dixi отвечает:\n\n{reply}", reply_markup=get_menu_keyboard())
            else:
                await message.answer(f"❌ Ошибка OpenRouter: {response.status_code} - {response.text}", reply_markup=get_menu_keyboard())
    except Exception as e:
        await message.answer(f"❌ Ошибка при обращении к Dixi: {str(e)}", reply_markup=get_menu_keyboard())

@router.message(lambda message: message.text == "🤖 Dixi")
async def handle_dixi_button(message: types.Message):
    """Обработчик кнопки Dixi"""
    await cmd_dixi(message)
