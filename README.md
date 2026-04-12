# AI LLM Shop Bot

Telegram bot with AI capabilities using OpenRouter.

## Features

- Greeting and help commands
- Current time and date commands
- AI-powered responses via OpenRouter
- FastAPI backend for additional API access

## Setup

1. Clone the repository
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Copy `.env.example` to `.env` and fill in your tokens:
   - `TELEGRAM_BOT_TOKEN`: From BotFather
   - `OPENROUTER_API_KEY`: From OpenRouter

## Running

### Telegram Bot
```
python bot/main.py
```

### FastAPI Server
```
uvicorn api.main:app --reload
```

## Commands

- `/start` - Welcome message
- `/help` - Show help
- `/time` - Current time
- `/date` - Current date
- Any other text - AI response

## API Endpoints

- `GET /` - API status
- `POST /chat` - Chat with AI
- `GET /health` - Health check
