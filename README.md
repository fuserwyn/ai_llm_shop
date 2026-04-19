# ai_llm_shop

Telegram бот для работы с AI/LLM моделями через OpenRouter

## Возможности

- 🔍 **DeepSeek** - мощная модель для сложных технических задач
- 🤖 **Claude Haiku** - быстрая и умная модель от Anthropic
- 🕒 Показ текущего времени
- 📱 Удобное меню с кнопками
- ⚡ Быстрые ответы через OpenRouter API
- 💾 **История сообщений** - автоматическое сохранение всех сообщений в SQLite базу данных
- 📊 **Суммаризация чата** - анализ реальной истории общения (до 420 сообщений)

## Поддерживаемые модели через OpenRouter

1. **DeepSeek** - использует модель deepseek/deepseek-chat
2. **Claude Haiku** - использует модель anthropic/claude-3-haiku

## Команды бота

- `/start` - Начать работу
- `/help` - Справка по командам
- `/time` - Текущее время
- `/date` - Текущая дата
- `/deepseek` - Работа с моделью DeepSeek
- `/claude` - Работа с моделью Claude Haiku
- `/summarize` - Суммаризация последних 420 сообщений чата
- `/history_stats` - Статистика сохраненных сообщений
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
DEEPSEEK_MODEL=deepseek/deepseek-chat
CLAUDE_HAIKU_MODEL=anthropic/claude-3-haiku
```

4. Запустите бота:
```bash
python main.py
```

## Использование моделей

### DeepSeek
Доступен через:
- Команду `/deepseek`
- Кнопку "🔍 DeepSeek" в меню
- Прямые запросы через `/deepseek_ваш_вопрос`

### Claude Haiku
Доступен через:
- Команду `/claude`
- Кнопку "🤖 Claude Haiku" в меню
- Прямые запросы через `/claude_ваш_вопрос`

## История сообщений

Бот автоматически сохраняет все сообщения в локальную SQLite базу данных (`chat_history.db`):
- Сохраняются как сообщения пользователей, так и ответы бота
- Для каждого сообщения сохраняется: текст, отправитель, время отправки
- История используется для суммаризации чата командой `/summarize`
- Просмотр статистики: `/history_stats`

## Суммаризация чата

Команда `/summarize` анализирует последние 420 сообщений из реальной истории общения:
- Использует модель DeepSeek через OpenRouter
- Анализирует темы, ключевые моменты и обсуждения
- Предоставляет структурированную суммаризацию на русском языке

## Тестирование

Запустите тесты:
```bash
pytest tests/
```

## Структура базы данных

```sql
CREATE TABLE messages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    chat_id INTEGER NOT NULL,
    user_id INTEGER NOT NULL,
    username TEXT,
    message_text TEXT NOT NULL,
    is_bot BOOLEAN NOT NULL,
    timestamp DATETIME NOT NULL
);
```