"""
Модуль для работы с файлами и директориями.

Этот модуль содержит класс FileSystemManager, который предоставляет \
методы для создания, чтения и управления файлами и директориями. \
Класс поддерживает использование заменителей в путях, что позволяет \
автоматически формировать имена файлов и директорий на основе \
текущего времени.

### Основные методы класса FileSystemManager:
- get_full_path_with_placeholders: Формирует полный путь к файлу или \
  директории с поддержкой заменителей.
- get_full_path: Формирует полный путь к файлу или директории.
- create_dir_or_file: Создает директорию или файл по указанному пути, \
  поддерживает заменители.

### Заменители:
Поддерживаются следующие заменители для формирования имен файлов и директорий:
- `<<Y>>`: Формирует название директории или файла по текущему году.
- `<<M>>`: Формирует название директории или файла по текущему месяцу.
- `<<Y-M-D>>`: Формирует название директории или файла по дате создания.

### Пример использования:
```python
manager = FileSystemManager()
full_path = \
manager.get_full_path_with_placeholders("logs/<<Y>>/<<M>>/<<Y-M-D>>.log")
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

    __placeholders = {
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
    __default_encoding = "utf-8"

    def get_full_path(self, path: str, is_placeholder: bool = False) -> str:
        """
        Формирует полный путь к файлу или директории с поддержкой заменителей.
        
        ### Аргументы:
        - path (str): Путь до нужной директории или файла от корня проекта. \
          Формат передаваемого пути должен быть "utils/timetools/tools" для \
          директории или "utils/timetools/tools/file.log" для файла.
        - is_placeholder (bool, optional): Флаг, указывающий, \
          нужно ли заменять заменители в пути. По умолчанию False.
        
        ### Примеры заменителей:
        - `<<Y>>` — Формирует название директории или файла по текущему году.
        - `<<M>>` — Формирует название директории или файла по текущему месяцу.

        ### Исключения:
        - ValueError: Если аргумент "path" не является строкой, \
          либо аргумент "is_placeholder" не является bool, либо путь содержит \
          недопустимые символы в качестве разделителей.
        """

        self.__validate_get_full_path_args(path, is_placeholder)

        input_path = (
            self.__replace_placeholders_in_path(path)
            if is_placeholder
            else path
            )

        return os.path.join(os.getcwd(), *input_path.split("/"))

    def create_dir_or_file(
        self, path: str, content: str = "", is_placeholder: bool = False
        ) -> None:
        """
        Создает директорию или файл по указанному пути.
        
        Поддерживает заменители. Для их использования необходимо 
        установить флаг "is_placeholder" в "True" и передать путь в формате
        "logs/<<Y>>/<<M>>".

        ### Аргументы:
        - path (str): Путь до нужной директории или файла от корня проекта. \
          Формат передаваемого пути должен быть "utils/timetools/tools" для \
          директории или "utils/timetools/tools/file.log" для файла.
        - content (str, optional): Содержимое файла (по умолчанию "").
        - is_placeholder (bool, optional): Флаг, указывающий, \
          нужно ли заменять заменители в пути. По умолчанию False.
        """

        full_path = self.get_full_path(path, is_placeholder)

        if '.' in os.path.basename(full_path):
            if not isinstance(content, str):
                content = ""

            os.makedirs(os.path.dirname(full_path), exist_ok=True)

            if not self.check_dir_or_file_exists(full_path):
                return None

            with open(full_path, "a", encoding=self.__default_encoding) as file:
                file.write(content)
        else:
            os.makedirs(full_path, exist_ok=True)

    def check_dir_or_file_exists(self, path: str) -> bool:
        """Проверка существования директории."""
        return os.path.exists(self.get_full_path(path))

    def list_files_in_dir(self, path: str) -> list:
        """Получение списка файлов в директории, указанной по пути."""
        return (
            os.listdir(self.get_full_path(path))
            if self.check_dir_or_file_exists(path)
            else []
            )

    def __replace_placeholders_in_path(self, path: str) -> str:
        """Заменяет все заменители в пути, если они есть."""

        for _, placeholder in self.__placeholders.items():
            placeholder_key = placeholder.get("placeholder")
            if placeholder_key in path:
                path = path.replace(placeholder_key, placeholder.get("func"))

        return path

    def __validate_get_full_path_args(self, path: str, is_placeholder: bool) \
        -> None:
        """Проверка параметров перед настройкой логирования."""

        if not path:
            raise ValueError("Аргумент 'path' не может быть пустым.")

        if not isinstance(path, str):
            raise ValueError(f"Аргумент 'path' должен быть строкой, \
                             а был передан тип '{type(path)}'")

        if path in ("\\", "\"", "|", ":", "*", "?", "<", ">", " ", "'", '"'):
            raise ValueError("В качестве разделителя директорий в аргументе \
                             'path' необходимо использовать '/'.")

        if not isinstance(is_placeholder, bool):
            raise ValueError(f"Аргумент 'is_placeholder' должен быть bool, \
                             а был передан тип '{type(is_placeholder)}'")
