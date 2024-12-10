"""
Модуль для работы с файлами и директориями.

Этот модуль содержит класс `FileSystemManager`, который предоставляет 
методы для создания, чтения и управления файлами и директориями. 
Класс поддерживает использование заменителей в путях, что позволяет 
автоматически формировать имена файлов и директорий на основе 
текущего времени.

### Основные методы класса `FileSystemManager`:
- `get_full_path_with_placeholders`: Формирует полный путь к файлу или 
  директории с поддержкой заменителей.
- `get_full_path`: Формирует полный путь к файлу или директории.
- `create_dir_or_file`: Создает директорию или файл по указанному пути, 
  поддерживает заменители.

### Заменители:
Поддерживаются следующие заменители для формирования имен файлов и директорий:
- `<<Y>>`: Формирует название директории или файла по текущему году.
- `<<M>>`: Формирует название директории или файла по текущему месяцу.
- `<<Y-M-D>>`: Формирует название директории или файла по дате создания.

### Пример использования:
```python
manager = FileSystemManager()
full_path = manager.get_full_path_with_placeholders("logs/<<Y>>/<<M>>/<<Y-M-D>>.log")
print(full_path)  # Выводит: "logs/2023/05/2023-05-01.log"
"""

import os

from utils.time_tools import timetools


class FileSystemManager:
    """
    Класс для работы с файлами и директориями. Поддерживает заменители.
    
    Заменители — это значения внутри пути, которые будут вызывать 
    соответствующие функции для автоматического формирования имен файлов и 
    директорий.
    
    Заменители полезно использовать для создания путей к файлам и 
    директориям, которые должны зависеть от текущего времени. Например, 
    файл или директория должны быть созданы с названием по текущему году.
    
    ### Поддерживаются следующие заменители:
    - `<<Y>>` — Формирует название директории или файла по году создания.
    - `<<M>>` — Формирует название директории или файла по месяцу создания.
    - `<<Y-M-D>>` — Формирует название директории или файла по дате создания.
    
    ### Пример использования:
    ```python
    manager = FileSystemManager()
    manager.create_dir_or_file("logs/<<Y>>/<<M>>/schema/<<Y-M-D>>.log")
    # Создает директорию logs/2024/June/2024-06-30.log
    ```
    """

    placeholders = {
        "date": {
            "placeholder": "<<Y-M-D>>",
            "func": timetools.get_current_time("%Y-%m-%d")
        },
        "year": {
            "placeholder": "<<Y>>",
            "func": timetools.get_current_time("%Y")
        },
        "month": {
            "placeholder": "<<M>>",
            "func": timetools.get_current_time("%B")
        }
    }
    sep_in_path = "/"

    def get_full_path_with_placeholders(self, path: str) -> str:
        """
        Формирует полный путь к файлу или директории с поддержкой заменителей.
        
        ### Примеры заменителей:
        - `<<Y>>` — Формирует название директории или файла по текущему году.
        - `<<M>>` — Формирует название директории или файла по текущему месяцу.
        
        ### Аргументы:
        - `path` (str): Путь в формате "utils.timetools.tools".
        """

        path = self._replace_placeholders_in_path(path)
        return os.path.join(os.getcwd(), *path.split(self.sep_in_path))

    def get_full_path(self, path: str, is_placeholder: bool = False) -> str:
        """
        Формирует полный путь к файлу или директории.
        
        ### Аргументы:
        - `path` (str): Путь до нужной директории или файла от корня проекта.
          Формат передаваемого пути должен быть "utils/timetools/tools" для 
          директории или "utils/timetools/tools/file.log" для файла.
        - `is_placeholder` (bool, optional): Флаг, указывающий, 
          нужно ли заменять заменители в пути. По умолчанию `False`.
        """

        return (
            self.get_full_path_with_placeholders(path)
            if is_placeholder
            else os.path.join(os.getcwd(), *path.split(self.sep_in_path))
        )

    def create_dir_or_file(
        self, path: str, content: str = "", is_placeholder: bool = False
        ) -> None:
        """
        Создает директорию или файл по указанному пути.
        
        Поддерживает заменители. Для их использования необходимо 
        установить флаг `is_placeholder` в `True` и передать путь в формате
        "logs/<<Y>>/<<M>>".
        
        ### Аргументы:
        - `path` (str): Путь до нужной директории или файла от корня проекта.
          Формат передаваемого пути должен быть "utils/timetools/tools" для 
          директории или "utils/timetools/tools/file.log" для файла.
        - `is_placeholder` (bool, optional): Флаг, указывающий, 
          нужно ли заменять заменители в пути. По умолчанию `False`.
        """

        full_path = self.get_full_path(path, is_placeholder)

        if '.' in os.path.basename(full_path):
            os.makedirs(os.path.dirname(full_path), exist_ok=True)
            with open(full_path, "a", encoding="utf-8") as file:
                file.write(content)
        else:
            os.makedirs(full_path, exist_ok=True)

    def _replace_placeholders_in_path(self, path: str) -> str:
        """Заменяет все заменители в пути, если они есть."""

        for _, placeholder in self.placeholders.items():
            placeholder_str = placeholder["placeholder"]
            if placeholder_str in path:
                path = path.replace(placeholder_str, placeholder["func"])

        return path
