import logging
from aiogram import Router, types
from aiogram.filters import Command
from app.services.deepseek_service import deepseek_service

logger = logging.getLogger(__name__)
router = Router()


@router.message(Command("deepseek"))
async def deepseek_command(message: types.Message):
    """Обработчик команды /deepseek"""
    # Получаем текст после команды
    user_text = message.text.replace("/deepseek", "").strip()
    
    if not user_text:
        await message.answer(
            "Пожалуйста, напишите ваш вопрос после команды /deepseek\n"
            "Например: /deepseek Что такое искусственный интеллект?"
        )
        return
    
    # Отправляем сообщение о обработке
    processing_msg = await message.answer("🤔 Думаю над ответом...")
    
    try:
        # Получаем ответ от DeepSeek
        response = await deepseek_service.chat_completion(user_text)
        
        if response:
            # Обрезаем ответ если слишком длинный (Telegram ограничение)
            if len(response) > 4000:
                response = response[:4000] + "..."
            
            await processing_msg.edit_text(f"💭 {response}")
        else:
            await processing_msg.edit_text(
                "❌ Произошла ошибка при обращении к AI. Попробуйте позже."
            )
            
    except Exception as e:
        logger.error(f"Error in deepseek command: {e}")
        await processing_msg.edit_text(
            "❌ Произошла внутренняя ошибка. Попробуйте позже."
        )