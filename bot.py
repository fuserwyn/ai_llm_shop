from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.utils import executor
import logging

logging.basicConfig(level=logging.INFO)

API_TOKEN = 'YOUR_BOT_TOKEN'

bot = Bot(token=API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.reply("Hi! I'm a bot.")

@dp.message_handler(commands=['help'])
async def send_help(message: types.Message):
    await message.reply("Available commands: /start, /help, /newcmd")

@dp.message_handler(commands=['newcmd'])
async def new_command(message: types.Message):
    await message.reply("This is a new command!")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)