import logging
from aiogram import types
from aiogram.dispatcher import Dispatcher

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

async def start_handler(message: types.Message):
    logger.info(f'Получено сообщение от пользователя {message.from_user.id}')
    await message.reply('Привет!')

async def echo_handler(message: types.Message):
    logger.info(f'Эхо сообщение от пользователя {message.from_user.id}: {message.text}')
    await message.reply(message.text)

def register_handlers(dp: Dispatcher):
    dp.register_message_handler(start_handler, commands=['start'])
    dp.register_message_handler(echo_handler)
    logger.info('Обработчики зарегистрированы')
