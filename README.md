# ai_llm_shop

Telegram бот для работы с AI/LLM моделями с интеграцией OpenRouter через Дикси.

## Возможности

- 🤖 Команды для навигации (/start, /help, /time, /menu)
- 🔌 Интеграция с OpenRouter API
- 💬 AI ассистент Дикси (/dixi команда)
- 🎛 Интерактивное меню с кнопками
- 🚀 FastAPI веб-сервер

## Настройка

1. Клонируйте репозиторий
2. Установите зависимости:
   ```bash
   pip install -r requirements.txt
   ```
3. Создайте файл `.env`:
   ```env
   BOT_TOKEN=your_telegram_bot_token
   ADMIN_IDS=123456789,987654321
   OPENROUTER_API_KEY=your_openrouter_api_key
   OPENROUTER_MODEL=openai/gpt-3.5-turbo  # опционально
   ```
4. Получите API ключ на [OpenRouter](https://openrouter.ai/)
5. Запустите бота:
   ```bash
   python main.py
   ```

## Использование Дикси

- Используйте команду `/dixi <ваш вопрос>`
- Или нажмите кнопку "🤖 Дикси" в меню
- Дикси использует OpenRouter API для генерации ответов

## Команды

- `/start` - Начать работу
- `/help` - Справка по командам
- `/time` - Текущее время
- `/dixi <текст>` - Задать вопрос Дикси
- `/openrouter <текст>` - Альтернативная команда для Дикси
- `/menu` - Показать меню