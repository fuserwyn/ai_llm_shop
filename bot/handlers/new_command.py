from aiogram import Router, types
from aiogram.filters import Command

router = Router()

@router.message(Command('new'))
async def new_command_handler(message: types.Message):
    await message.answer('This is a new command!')