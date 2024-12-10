"""
Настройка конфигурации логирования и установка логгера.

Этот модуль содержит функции и настройки, необходимые для создания и 
конфигурации логгера. Он позволяет настраивать формат логов, уровень 
логирования, кодировку и структуру директорий для хранения логов.

### Пример настройки логирования:
```python
from utils.logging.config import configure_logging

logger = setup_logger(<module_name>, <file_name>)
```

### Пример созданной файловой структуры:
```
root
├── logs
│   ├── 2024
│   │   ├── June
│   │   │   ├── default
│   │   │   │   ├── 2024-06-29.log
│   │   │   │   └── 2024-06-30.log
```

### Пример использования логгера:
```python
logger = setup_logger(<module_name>, <file_name>)

...

try:
    ...
    logger.info("Информационное сообщение")
except Exception as e:
    logger.error(f"Ошибка: {e}")
```

### Примечания:
- Логи организованы по директориям, основанным на текущем времени, 
  что позволяет легко управлять и находить логи по дате.
- Поддерживаются заменители для формирования имен файлов и директорий 
  в зависимости от времени создания.
"""

import logging

from utils.fs.manager import FileSystemManager
from utils.logging.build import (
    LoggerBuilder, DEFAULT_LOG_ENCODING, DEFAULT_LOG_FORMAT
    )


def handle_log_directory_creation(module_name: str, file_name: str) -> str:
    """
    Обработчик для создания всех необходимых директорий и файла для логов.
    
    ### Аргументы:
    - `module_name` (str): Название логируемого модуля.
    - `file_name` (str): Имя лог-файла.
    
    ### Возвращает:
    - `str`: Полный путь до созданного лог-файла или директории.
    """

    dir_path = f"logs/<<Y>>/<<M>>/{module_name}/{file_name}.log"

    manager = FileSystemManager()
    manager.create_dir_or_file(dir_path, is_placeholder=True)

    return manager.get_full_path(dir_path, is_placeholder=True)


def setup_logger(
    module_name: str = "default",
    file_name: str = "<<Y-M-D>>",
    log_format: str = DEFAULT_LOG_FORMAT,
    log_level: int = logging.INFO,
    encoding: str = DEFAULT_LOG_ENCODING,
    logger_name: str = "vk_match_sensei"
) -> logging.Logger:
    """
    Настройка логирования для указанного модуля.
    
    Данная функция создает и настраивает логгер для указанного модуля.
    
    ### Аргументы:
    - `module_name` (str): Название логируемого модуля. Используется для 
      создания структуры директорий для логов. По умолчанию "default".
    - `file_name` (str): Имя лог-файла. Может содержать заменители для 
      даты. По умолчанию "<<Y-M-D>>".
    - `log_format` (str): Формат записи логов. По умолчанию используется 
      `DEFAULT_LOG_FORMAT`.
    - `log_level` (int): Уровень логирования. По умолчанию `logging.INFO`.
    - `encoding` (str): Кодировка для записи логов. По умолчанию "utf-8".
    - `logger_name` (str): Имя логгера. По умолчанию "vk_match_sensei".
    
    ### Возвращает:
    - `logging.Logger`: Настроенный логгер, готовый к использованию.
    
    ### Формат пути для лог-файла: 
    `logs/<<Y>>/<<M>>/{module_name}/{file_name}.log`, где:
    - `logs` — Корневая директория для логов.
    - `<<Y>>` — Формирует название директории по году создания.
    - `<<M>>` — Формирует название директории по месяцу создания.
    - `{module_name}` — Название логируемого модуля.
    - `{file_name}` — Имя лог-файла.
    """

    log_file_path = handle_log_directory_creation(module_name, file_name)

    logger_builder = LoggerBuilder()

    logger = logger_builder.create_logger(logger_name, log_level)

    file_handler = logger_builder.create_logger_file_handler(
        log_file_path, log_level, encoding
        )
    file_handler.setFormatter(
        logger_builder.create_logger_formatter(log_format)
        )

    logger.addHandler(file_handler)

    return logger
