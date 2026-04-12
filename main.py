from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.utils import executor
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
API_TOKEN = 'YOUR_BOT_TOKEN_HERE'
bot = Bot(token=API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

# Define states
class Form(StatesGroup):
    name = State()
    age = State()
    location = State()

@dp.message_handler(commands=['start'])
async def cmd_start(message: types.Message):
    await message.reply("Hi! I'm a bot. Use /register to start registration.")

@dp.message_handler(commands=['register'])
async def cmd_register(message: types.Message):
    await Form.name.set()
    await message.reply("What is your name?")

@dp.message_handler(state=Form.name)
async def process_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['name'] = message.text
    
    await Form.next()
    await message.reply("How old are you?")

@dp.message_handler(state=Form.age)
async def process_age(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['age'] = message.text
    
    await Form.next()
    await message.reply("Where do you live?")

@dp.message_handler(state=Form.location)
async def process_location(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['location'] = message.text
        
        # You can process the data here (save to database, etc.)
        await message.reply(f"Thank you! Registered:\n"
                            f"Name: {data['name']}\n"
                            f"Age: {data['age']}\n"
                            f"Location: {data['location']}")
    
    await state.finish()

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)