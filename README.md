# AI LLM Shop

Telegram bot shop with AI/LLM integration.

## Features

- Product catalog
- Shopping cart
- Order processing
- AI-powered recommendations
- Payment integration

## Tech Stack

- Python 3.11+
- aiogram for Telegram bot
- FastAPI for webhooks
- SQLAlchemy for database
- Redis for caching

## Installation

1. Clone the repository:
```bash
git clone https://github.com/fuserwyn/ai_llm_shop.git
cd ai_llm_shop
```

2. Create virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Configure environment variables:
```bash
cp .env.example .env
# Edit .env with your settings
```

5. Run the bot:
```bash
python main.py
```

## License

MIT