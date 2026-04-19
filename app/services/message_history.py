import sqlite3
from datetime import datetime
from typing import List, Dict, Any, Optional
import json
import os
from dataclasses import dataclass, asdict

@dataclass
class ChatMessage:
    """Класс для представления сообщения чата"""
    id: Optional[int] = None
    chat_id: int = 0
    user_id: int = 0
    username: str = ""
    message_text: str = ""
    is_bot: bool = False
    timestamp: datetime = None
    
    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now()

class MessageHistoryService:
    """Сервис для работы с историей сообщений"""
    
    def __init__(self, db_path: str = "chat_history.db"):
        self.db_path = db_path
        self._init_database()
    
    def _init_database(self):
        """Инициализация базы данных"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Создаем таблицу для сообщений
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            chat_id INTEGER NOT NULL,
            user_id INTEGER NOT NULL,
            username TEXT,
            message_text TEXT NOT NULL,
            is_bot BOOLEAN NOT NULL,
            timestamp DATETIME NOT NULL
        )
        ''')
        
        # Создаем индекс для быстрого поиска по chat_id и timestamp
        cursor.execute('''
        CREATE INDEX IF NOT EXISTS idx_chat_timestamp 
        ON messages (chat_id, timestamp DESC)
        ''')
        
        conn.commit()
        conn.close()
    
    def save_message(self, message: ChatMessage) -> int:
        """Сохраняет сообщение в базу данных"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
        INSERT INTO messages (chat_id, user_id, username, message_text, is_bot, timestamp)
        VALUES (?, ?, ?, ?, ?, ?)
        ''', (
            message.chat_id,
            message.user_id,
            message.username,
            message.message_text,
            1 if message.is_bot else 0,
            message.timestamp.isoformat()
        ))
        
        message_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return message_id
    
    def get_recent_messages(self, chat_id: int, limit: int = 420) -> List[ChatMessage]:
        """Получает последние сообщения из чата"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
        SELECT id, chat_id, user_id, username, message_text, is_bot, timestamp
        FROM messages
        WHERE chat_id = ?
        ORDER BY timestamp DESC
        LIMIT ?
        ''', (chat_id, limit))
        
        messages = []
        for row in cursor.fetchall():
            message = ChatMessage(
                id=row[0],
                chat_id=row[1],
                user_id=row[2],
                username=row[3],
                message_text=row[4],
                is_bot=bool(row[5]),
                timestamp=datetime.fromisoformat(row[6])
            )
            messages.append(message)
        
        conn.close()
        
        # Возвращаем в хронологическом порядке (от старых к новым)
        return list(reversed(messages))
    
    def get_message_count(self, chat_id: int) -> int:
        """Получает количество сообщений в чате"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
        SELECT COUNT(*) FROM messages WHERE chat_id = ?
        ''', (chat_id,))
        
        count = cursor.fetchone()[0]
        conn.close()
        
        return count
    
    def clear_chat_history(self, chat_id: int) -> int:
        """Очищает историю сообщений для указанного чата"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
        DELETE FROM messages WHERE chat_id = ?
        ''', (chat_id,))
        
        deleted_count = cursor.rowcount
        conn.commit()
        conn.close()
        
        return deleted_count
    
    def export_to_json(self, chat_id: int, filepath: str) -> bool:
        """Экспортирует историю чата в JSON файл"""
        messages = self.get_recent_messages(chat_id, limit=1000)  # Большой лимит для экспорта
        
        data = {
            "chat_id": chat_id,
            "export_date": datetime.now().isoformat(),
            "message_count": len(messages),
            "messages": [asdict(msg) for msg in messages]
        }
        
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2, default=str)
            return True
        except Exception as e:
            print(f"Error exporting to JSON: {e}")
            return False

# Синглтон экземпляр для использования во всем приложении
_message_history_service = None

def get_message_history_service() -> MessageHistoryService:
    """Получает экземпляр сервиса истории сообщений"""
    global _message_history_service
    if _message_history_service is None:
        _message_history_service = MessageHistoryService()
    return _message_history_service