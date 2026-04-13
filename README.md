# ai_llm_shop

Telegram бот для работы с AI/LLM моделями через OpenRouter

## Возможности

- 🤖 **Дикси** - AI ассистент на базе GPT моделей
- 🔍 **DeepSeek** - мощная модель для сложных технических задач
- 🕒 Показ текущего времени
- 📱 Удобное меню с кнопками
- ⚡ Быстрые ответы через OpenRouter API

## Поддерживаемые модели через OpenRouter

1. **Дикси** - использует модель из конфигурации (по умолчанию: openai/gpt-3.5-turbo)
2. **DeepSeek** - использует модель deepseek/deepseek-chat

## Команды бота

- `/start` - Начать работу
- `/help` - Справка по командам
- `/time` - Текущее время
- `/dixi` - Общение с AI ассистентом Дикси
- `/deepseek` - Работа с моделью DeepSeek
- `/menu` - Показать меню

## Установка

1. Клонируйте репозиторий:
```bash
git clone https://github.com/fuserwyn/ai_llm_shop.git
cd ai_llm_shop
```

2. Установите зависимости:
```bash
pip install -r requirements.txt
```

3. Создайте файл `.env`:
```env
BOT_TOKEN=your_telegram_bot_token
OPENROUTER_API_KEY=your_openrouter_api_key
# Опционально:
OPENROUTER_MODEL=openai/gpt-3.5-turbo
DEEPSEEK_MODEL=deepseek/deepseek-chat
```

4. Запустите бота:
```bash
python main.py
```

## Использование DeepSeek

DeepSeek доступен через:
- Команду `/deepseek`
- Кнопку "🔍 DeepSeek" в меню
- Прямые запросы через `/deepseek_ваш_вопрос`

## Тестирование

Запустите тесты:
```bash
pytest tests/
```