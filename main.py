from fastapi import FastAPI
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm.storage.memory import MemoryStorage
import logging
import asyncio
from config import BOT_TOKEN, WEBHOOK_URL, WEBHOOK_PATH, PORT

# Initialize FastAPI app
app = FastAPI()

# Initialize bot and dispatcher
bot = Bot(token=BOT_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Webhook route
@app.post(WEBHOOK_PATH)
async def webhook(request: types.Update):
    update = request.json()
    await dp.process_update(update)
    return {"ok": True}

# Startup event
@app.on_event("startup")
async def on_startup():
    webhook_info = await bot.get_webhook_info()
    if webhook_info.url != WEBHOOK_URL:
        await bot.set_webhook(
            url=WEBHOOK_URL,
            drop_pending_updates=True
        )
    logger.info("Bot started")

# Shutdown event
@app.on_event("shutdown")
async def on_shutdown():
    await bot.delete_webhook()
    logger.info("Bot stopped")

# Health check
@app.get("/")
async def health_check():
    return {"status": "ok"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=PORT)