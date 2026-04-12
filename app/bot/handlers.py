from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message

from app.database import get_session
from app.models import User
from sqlmodel import select

router = Router()


@router.message(CommandStart())
async def start_handler(message: Message):
    async with get_session() as session:
        user = await session.exec(
            select(User).where(User.telegram_id == message.from_user.id)
        ).first()
        if not user:
            user = User(
                telegram_id=message.from_user.id,
                username=message.from_user.username,
                full_name=message.from_user.full_name,
            )
            session.add(user)
            await session.commit()
        await message.answer(f"Hello, {user.full_name}!")


@router.message(F.text)
async def echo_handler(message: Message):
    await message.answer(message.text)
