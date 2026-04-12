# AI LLM Shop Bot

Telegram bot with AI assistant capabilities using OpenRouter.

## Features
- Greeting and help commands
- Current time and date commands
- AI chat via OpenRouter (GPT-3.5-turbo)
- FastAPI backend for chat API

## Setup
1. Clone repository
2. Install dependencies: `pip install -r requirements.txt`
3. Copy `.env.example` to `.env` and fill in your tokens:
   - `TELEGRAM_BOT_TOKEN` from BotFather
   - `OPENROUTER_API_KEY` from OpenRouter
4. Run bot: `python bot/main.py`
5. Run API: `uvicorn api.main:app --reload`

## Commands
- `/start` - Start bot
- `/help` - Show help
- `/time` - Current time
- `/date` - Current date
- Any text - AI chat response

## API Endpoints
- `GET /` - Health check
- `POST /chat` - AI chat endpoint
