import datetime
import os
from typing import Dict, Optional


# Имитация языковой модели (упрощенная версия)
class SimpleChatModel:
    """
    Упрощенная модель чата с предопределенными ответами.
    
    Attributes:
        responses (Dict[str, str]): Словарь с предопределенными ответами на пользовательские запросы.
    """
    def __init__(self) -> None:
        """Инициализирует модель с предопределенными ответами."""
        self.responses: Dict[str, str] = {
            "привет": "Привет! Как дела?",
            "как дела": "У меня все отлично! Чем могу помочь?",
            "пока": "До свидания! Возвращайтесь снова.",
            "помощь": "Я могу ответить на простые вопросы. Попробуйте сказать 'привет', 'как дела' или 'пока'."
        }
    
    def get_response(self, user_input: str) -> str:
        """
        Возвращает ответ модели на пользовательский ввод.
        
        Args:
            user_input (str): Ввод пользователя.
        
        Returns:
            str: Ответ модели или сообщение о непонимании.
        """
        user_input = user_input.lower().strip()
        return self.responses.get(user_input, "Извините, я не понимаю этот вопрос. Попробуйте спросить что-то другое.")


def show_time() -> None:
    """Выводит текущее время в формате HH:MM:SS."""
    current_time = datetime.datetime.now().strftime("%H:%M:%S")
    print(f"Текущее время: {current_time}")


def show_date() -> None:
    """Выводит текущую дату в формате DD.MM.YYYY."""
    current_date = datetime.datetime.now().strftime("%d.%m.%Y")
    print(f"Сегодняшняя дата: {current_date}")


def show_help() -> None:
    """Выводит меню доступных команд."""
    print("\n=== Доступные команды ===")
    print("time - показать текущее время")
    print("date - показать текущую дату")
    print("help - показать это меню помощи")
    print("start - начать общение с моделью")
    print("exit - выйти из приложения")
    print("=======================\n")


def chat_with_model() -> None:
    """Запускает интерактивный режим общения с чат-моделью."""
    model = SimpleChatModel()
    print("\n=== Режим общения с моделью ===")
    print("Напишите 'выход' чтобы вернуться в главное меню")
    print("Модель готова к общению!\n")
    
    while True:
        user_input = input("Вы: ").strip()
        
        if user_input.lower() == "выход":
            print("Выход из режима общения...\n")
            break
        
        response = model.get_response(user_input)
        print(f"Модель: {response}")


def main() -> None:
    """Основная функция приложения, обрабатывающая команды пользователя."""
    print("=== Приложение с командами и чат-моделью ===")
    print("Введите команду (time, date, help, start, exit)")
    
    while True:
        command = input("\nВведите команду: ").strip().lower()
        
        if command == "time":
            show_time()
        elif command == "date":
            show_date()
        elif command == "help":
            show_help()
        elif command == "start":
            chat_with_model()
        elif command == "exit":
            print("Выход из приложения...")
            break
        else:
            print("Неизвестная команда. Введите 'help' для списка команд.")


if __name__ == "__main__":
    main()
