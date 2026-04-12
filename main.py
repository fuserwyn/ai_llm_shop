import asyncio
import logging
from datetime import datetime
from typing import Optional

from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import Message
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(title="AI LLM Shop")

# Initialize bot and dispatcher (replace with your token)
BOT_TOKEN = "YOUR_BOT_TOKEN_HERE"  # TODO: Set from environment
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# In-memory storage for demo (replace with DB in production)
user_sessions = {}


class ChatRequest(BaseModel):
    user_id: int
    message: str


class ChatResponse(BaseModel):
    response: str


@app.get("/")
def read_root():
    return {"message": "AI LLM Shop API is running"}


@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    """Endpoint for chat interactions"""
    # Simple echo for demo (replace with LLM integration)
    response = f"Echo: {request.message}"
    
    # Store in session (optional)
    if request.user_id not in user_sessions:
        user_sessions[request.user_id] = []
    user_sessions[request.user_id].append({
        "user": request.message,
        "bot": response
    })
    
    return ChatResponse(response=response)


@app.get("/history/{user_id}")
def get_history(user_id: int):
    """Get chat history for a user"""
    return user_sessions.get(user_id, [])


# Telegram bot handlers
@dp.message(Command("start"))
async def cmd_start(message: Message):
    await message.answer(
        "Welcome to AI LLM Shop!\n"
        "Available commands: /time, /date, /help"
    )


@dp.message(Command("help"))
async def cmd_help(message: Message):
    await message.answer(
        "Available commands:\n"
        "/start - Start the bot\n"
        "/time - Current time\n"
        "/date - Current date\n"
        "/help - This message"
    )


@dp.message(Command("time"))
async def cmd_time(message: Message):
    current_time = datetime.now().strftime("%H:%M:%S")
    await message.answer(f"Current time: {current_time}")


@dp.message(Command("date"))
async def cmd_date(message: Message):
    current_date = datetime.now().strftime("%Y-%m-%d")
    await message.answer(f"Current date: {current_date}")


@dp.message()
async def echo_message(message: Message):
    """Echo non-command messages (replace with LLM)"""
    await message.answer(f"You said: {message.text}")


async def start_bot():
    """Start the Telegram bot"""
    logger.info("Starting bot...")
    await dp.start_polling(bot)


def run_cli():
    """Run command-line interface"""
    print("=== Приложение с командами и чат-моделью ===")
    print("Введите команду (time, date, help, start, exit)")
    
    while True:
        try:
            command = input("\nВведите команду: ").strip().lower()
        except EOFError:
            print("\nInput stream closed. Exiting CLI.")
            break
        
        if command == "exit":
            print("Goodbye!")
            break
        elif command == "time":
            print(f"Current time: {datetime.now().strftime('%H:%M:%S')}")
        elif command == "date":
            print(f"Current date: {datetime.now().strftime('%Y-%m-%d')}")
        elif command == "help":
            print("Available commands: time, date, help, start, exit")
        elif command == "start":
            print("Welcome to AI LLM Shop CLI!")
        else:
            print(f"Unknown command: {command}. Type 'help' for list.")


def main():
    """Main entry point"""
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "--cli":
        # Run CLI mode
        run_cli()
    else:
        # Run bot + API (default)
        import uvicorn
        
        # Start bot in background
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        bot_task = loop.create_task(start_bot())
        
        # Start FastAPI
        uvicorn.run(app, host="0.0.0.0", port=8000, loop=loop)


if __name__ == "__main__":
    main()
