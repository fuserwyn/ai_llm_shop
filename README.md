# Simple Telegram Bot

A minimal Telegram bot built with aiogram and FastAPI (via aiohttp) that responds to three commands.

## Commands
- `/start` - Start the bot
- `/help` - Show help message
- `/date` - Show current date and time

## Setup
1. Copy `.env.example` to `.env` and set your `BOT_TOKEN` and `WEBHOOK_URL`.
2. Install dependencies: `pip install -r requirements.txt`
3. Run the bot: `python bot.py`

## Deployment
Configure your webhook URL in `.env` and ensure the server is accessible for Telegram webhooks.
