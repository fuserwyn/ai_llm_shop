# AI Telegram Bot

Бот с функциями помощника, отображением времени/даты и интеграцией с OpenRouter AI.

## Функции

- Приветствие и помощь (/start, /help)
- Показ текущего времени (/time)
- Показ текущей даты (/date)
- Ответы на вопросы через OpenRouter AI

## Установка

1. Клонируйте репозиторий
2. Установите зависимости:
   ```bash
   pip install -r requirements.txt
   ```
3. Создайте файл `.env` на основе `.env.example` и заполните токены

## Запуск

### Бот (Telegram)
```bash
python bot/main.py
```

### API (FastAPI)
```bash
uvicorn api.main:app --reload
```

## Переменные окружения

- `TELEGRAM_BOT_TOKEN` - Токен вашего Telegram бота от @BotFather
- `OPENROUTER_API_KEY` - API ключ от OpenRouter (https://openrouter.ai)

## Структура проекта

- `bot/main.py` - Основной код Telegram бота
- `api/main.py` - FastAPI приложение для веб-интерфейса
- `requirements.txt` - Зависимости Python
- `.env.example` - Шаблон файла с переменными окружения
