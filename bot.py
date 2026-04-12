import asyncio
import logging
import os
import sys
from pathlib import Path
from contextlib import asynccontextmanager

import aiofiles
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
from aiohttp import web

from config import settings
from handlers import router

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    stream=sys.stdout
)
logger = logging.getLogger(__name__)

# Global bot and dispatcher instances
bot = Bot(
    token=settings.BOT_TOKEN,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)
dp = Dispatcher(storage=MemoryStorage())
dp.include_router(router)

# Lock file path for polling mode
POLLING_LOCKFILE = Path("/tmp/telegram_bot_polling.lock")


def is_polling_lock_active() -> bool:
    """Check if polling lock file exists and is recent (within 60 seconds)."""
    if not POLLING_LOCKFILE.exists():
        return False
    try:
        mtime = POLLING_LOCKFILE.stat().st_mtime
        return (time.time() - mtime) < 60
    except Exception:
        return False


def acquire_polling_lock() -> bool:
    """Create lock file if not already active."""
    if is_polling_lock_active():
        return False
    try:
        POLLING_LOCKFILE.touch()
        return True
    except Exception:
        return False


def release_polling_lock() -> None:
    """Remove lock file."""
    try:
        if POLLING_LOCKFILE.exists():
            POLLING_LOCKFILE.unlink()
    except Exception:
        pass


async def start_polling() -> None:
    """Start bot in polling mode with lock mechanism."""
    import time
    
    if not acquire_polling_lock():
        logger.error(
            "Another polling instance appears to be running. "
            "If not, delete %s and restart.",
            POLLING_LOCKFILE
        )
        sys.exit(1)
    
    try:
        logger.info("Starting bot in polling mode...")
        await dp.start_polling(bot)
    finally:
        release_polling_lock()


async def start_webhook() -> None:
    """Start bot in webhook mode."""
    logger.info("Starting bot in webhook mode...")
    
    # Set webhook
    await bot.set_webhook(
        url=settings.WEBHOOK_URL,
        secret_token=settings.WEBHOOK_SECRET,
        drop_pending_updates=True
    )
    
    # Create aiohttp app
    app = web.Application()
    webhook_requests_handler = SimpleRequestHandler(
        dispatcher=dp,
        bot=bot,
        secret_token=settings.WEBHOOK_SECRET,
    )
    webhook_requests_handler.register(app, path=settings.WEBHOOK_PATH)
    setup_application(app, dp, bot=bot)
    
    # Start web server
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, settings.WEBHOOK_HOST, settings.WEBHOOK_PORT)
    await site.start()
    
    logger.info(f"Webhook server started on {settings.WEBHOOK_HOST}:{settings.WEBHOOK_PORT}")
    
    # Keep running
    await asyncio.Future()


@asynccontextmanager
async def lifespan(_):
    """Lifespan manager for webhook mode."""
    # Startup
    logger.info("Starting up...")
    yield
    # Shutdown
    logger.info("Shutting down...")
    await bot.session.close()


async def main() -> None:
    """Main entry point."""
    if settings.WEBHOOK_URL:
        await start_webhook()
    else:
        await start_polling()


if __name__ == "__main__":
    asyncio.run(main())
