from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from fastapi import FastAPI
import logging
import config
from app.handlers import commands_router, dixi_router

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize FastAPI app
app = FastAPI(title="AI LLM Shop Bot")

# Initialize bot and dispatcher
API_TOKEN = config.BOT_TOKEN
bot = Bot(token=API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)

# Include routers
dp.include_router(commands_router)
dp.include_router(dixi_router)

@app.get("/")
async def root():
    return {"message": "AI LLM Shop Bot is running"}

@app.get("/health")
async def health():
    return {"status": "healthy"}

@app.on_event("startup")
async def on_startup():
    logging.info("Starting bot polling...")
    # Start polling in background
    import asyncio
    asyncio.create_task(dp.start_polling(bot, skip_updates=True))

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
