from aiogram import Router, types
from aiogram.filters import Command

router = Router()

@router.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer("Welcome!")

@router.message(Command("help"))
async def cmd_help(message: types.Message):
    await message.answer("Help info")

@router.message(Command("newcmd"))
async def cmd_newcmd(message: types.Message):
    await message.answer("This is a new command added to the bot.")