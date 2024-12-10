"""
Модуль для утилит работы с временем.

Этот модуль предоставляет различные функции для манипуляции и обработки
временных данных.
"""

from datetime import datetime


class TimeTools:
    """Класс для работы с временными данными."""
    
    DEFAULT_TIME_FORMAT = "%Y-%m-%d %H:%M:%S"
    
    def get_current_time(self, format: str = DEFAULT_TIME_FORMAT) -> str:
        """Возвращает текущее время в указанном формате в виде строки."""
        current_datetime = self.get_current_datetime()
        return self.format_datetime_to_str_time(current_datetime, format)

    @staticmethod
    def get_current_datetime() -> datetime:
        """Возвращает текущее время в виде объекта `datetime`."""
        return datetime.now()

    @staticmethod
    def format_datetime_to_str_time(dt: datetime, format: str) -> str:
        """Форматирует объект `datetime` в строку в указанном формате."""
        return dt.strftime(format)
