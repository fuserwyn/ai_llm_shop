import asyncio
import logging
import sys
import os
from contextlib import asynccontextmanager

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from fastapi import FastAPI

from app.bot.handlers import router as bot_router
from app.bot.middlewares import DatabaseMiddleware
from app.database import create_db_and_tables, engine
from app.settings import settings

logging.basicConfig(level=logging.INFO, stream=sys.stdout)
logger = logging.getLogger(__name__)

USE_POLLING = os.getenv("USE_POLLING", "true").lower() == "true"

bot = Bot(token=settings.BOT_TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher(storage=MemoryStorage())
dp.include_router(bot_router)
dp.update.middleware(DatabaseMiddleware())


@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_db_and_tables()
    logger.info("Starting bot...")
    if USE_POLLING:
        asyncio.create_task(start_polling())
    else:
        raise ValueError("USE_POLLING must be set to 'true' in environment")
    yield
    logger.info("Shutting down bot...")
    await bot.session.close()
    await engine.dispose()


async def start_polling():
    await dp.start_polling(bot)


app = FastAPI(lifespan=lifespan)


@app.get("/health")
def health_check():
    return {"status": "ok"}
