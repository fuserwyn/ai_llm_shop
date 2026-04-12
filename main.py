from aiogram import Bot, Dispatcher, types
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.filters import Command
import logging
import config

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
API_TOKEN = config.BOT_TOKEN
bot = Bot(token=API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)

# Define states
class Form(StatesGroup):
    name = State()
    age = State()
    location = State()

@dp.message(Command('start'))
async def cmd_start(message: types.Message):
    await message.reply("Hi! I'm a bot. Use /register to start registration.")

@dp.message(Command('register'))
async def cmd_register(message: types.Message, state: FSMContext):
    await state.set_state(Form.name)
    await message.reply("What is your name?")

@dp.message(state=Form.name)
async def process_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(Form.age)
    await message.reply("How old are you?")

@dp.message(state=Form.age)
async def process_age(message: types.Message, state: FSMContext):
    await state.update_data(age=message.text)
    await state.set_state(Form.location)
    await message.reply("Where do you live?")

@dp.message(state=Form.location)
async def process_location(message: types.Message, state: FSMContext):
    data = await state.get_data()
    await message.reply(f"Thank you! Registered:\n"
                        f"Name: {data['name']}\n"
                        f"Age: {data['age']}\n"
                        f"Location: {data['location']}")
    await state.clear()

if __name__ == '__main__':
    dp.run_polling(bot, skip_updates=True)
