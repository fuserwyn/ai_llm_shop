# ai_llm_shop

Бот для работы с AI/LLM моделями, интегрированный с OpenRouter через Dixi.

## Команды

- `/start` - Начать работу с ботом
- `/help` - Показать список команд
- `/time` - Показать текущее время
- `/menu` - Показать меню с кнопками

## Интеграция с OpenRouter

Бот использует Dixi для обработки сообщений пользователя через OpenRouter API. Для работы требуется:

1. Установить переменную окружения `OPENROUTER_API_KEY`
2. Бот будет отвечать на сообщения пользователя с помощью AI модели.

## Запуск

```bash
pip install -r requirements.txt
python main.py
```

## Конфигурация

Создайте файл `.env`:
```
BOT_TOKEN=your_bot_token
ADMIN_IDS=123456789,987654321
OPENROUTER_API_KEY=your_openrouter_api_key
```