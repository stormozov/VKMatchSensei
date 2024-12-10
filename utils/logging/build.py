"""
Модуль для создания логгера.

Этот модуль содержит класс `LoggerBuilder`, который предоставляет методы для 
создания логгера, обработчика файлов и форматтера логов. Он позволяет 
настраивать логирование в приложении, включая уровень логирования, 
формат сообщений и кодировку.

### Класс:
- `LoggerBuilder`: Класс для создания логгера.

### Константы:
- `DEFAULT_LOG_ENCODING`: Стандартная кодировка для логов (по умолчанию "utf-8").
- `DEFAULT_LOG_FORMAT`: Стандартный формат записи логов, включающий 
  информацию о времени, имени логгера, уровне логирования и сообщении.

### Пример использования:
```python
from utils.logging.build import LoggerBuilder

logger_builder = LoggerBuilder("my_logger")
logger = logger_builder.create_logger()
file_handler = logger_builder.create_logger_file_handler("my_log.log")
formatter = logger_builder.create_logger_formatter()
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)
```
"""

import logging

DEFAULT_LOG_ENCODING = "utf-8"
DEFAULT_LOG_FORMAT = (f"%(asctime)s\n"
                      f"%(name)s\n"
                      f"|—— Путь до модуля (%(filename)s):\n%(pathname)s\n"
                      f"|—— Функция и строка: %(funcName)s:%(lineno)d\n"
                      f"|—— Уровень: [%(levelno)s — %(levelname)s]\n"
                      f"|—— Результат: %(message)s\n\n"
                      )


class LoggerBuilder:
    """Класс для создания логгера."""

    def create_logger(self, logger_name: str, log_level: str) -> logging.Logger:
        """Создает логгер с указанным именем."""

        logger = logging.getLogger(logger_name)
        logger.setLevel(log_level)

        return logger

    def create_logger_file_handler(
        self,
        log_file: str,
        log_level: int = logging.INFO,
        encoding: str = DEFAULT_LOG_ENCODING
    ) -> logging.FileHandler:
        """Создает обработчик для записи логов в файл."""

        file_handler = logging.FileHandler(log_file, encoding=encoding)
        file_handler.setLevel(log_level)

        return file_handler

    def create_logger_formatter(self, log_format: str = DEFAULT_LOG_FORMAT) \
        -> logging.Formatter:
        """Создает форматтер для записи логов."""
        formatter = logging.Formatter(log_format)
        return formatter
