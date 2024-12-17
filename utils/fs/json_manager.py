"""Менеджер для работы с JSON-файлами."""

import os
import json

from services.formatters.module_formatters import get_module_part
from utils.fs.fs_manager import FileSystemManager
from utils.logging.setup import setup_logger


class JSONManager:
    """
    Менеджер для работы с JSON-файлами.

    ### Доступные методы:
    - write_json_file: Запись JSON-файла.
    - read_json_file: Чтение JSON-файла и получение его содержимого в формате \
      словаря.
    - delete_json_file: Удаление JSON-файла.
    - check_json_file_exists: Проверка существования JSON-файла.
    - get_bot_settings_from_json: Получение настроек бота из JSON-файла.
    """

    __DEFAULT_ENCODING = "utf-8"
    __FS_MANAGER = FileSystemManager()

    def __init__(self) -> None:
        self.logger = setup_logger(
            module_name=get_module_part(__name__, idx=0), logger_name=__name__
            )

    def write_json_file(self, file_path: str, content: dict) -> None:
        """
        Запись JSON-файла.
        
        Формат передаваемого пути должен быть "utils/timetools/tools" для 
        директории или "utils/timetools/tools/file.log" для файла.
        """

        if self._validate_content_for_write(content) is not None:
            return None

        file_path = self.__FS_MANAGER.get_full_path(file_path)

        if not self.__FS_MANAGER.check_dir_or_file_exists(file_path):
            self.logger.error(
                "Директория %s не существует. Запись JSON-файла невозможна.",
                file_path
                )
            return None

        with open(file_path, "w", encoding=self.__DEFAULT_ENCODING) as file:
            json.dump(content, file)

        return None

    def read_json_file(self, file_path: str) -> dict | None:
        """
        Чтение JSON-файла и получение его содержимого в формате словаря.

        Формат передаваемого пути должен быть "utils/timetools/tools" для
        директории или "utils/timetools/tools/file.log" для файла.
        """

        file_path = self.__FS_MANAGER.get_full_path(file_path)

        if not self.__FS_MANAGER.check_dir_or_file_exists(file_path):
            return None

        with open(file_path, "r", encoding=self.__DEFAULT_ENCODING) as file:
            return json.load(file)

    def delete_json_file(self, file_path: str) -> None:
        """
        Удаление JSON-файла.
        
        Формат передаваемого пути должен быть "utils/timetools/tools" для 
        директории или "utils/timetools/tools/file.log" для файла.
        """

        file_path = self.__FS_MANAGER.get_full_path(file_path)

        if not self.__FS_MANAGER.check_dir_or_file_exists(file_path):
            return

        os.remove(file_path)

    def get_bot_settings_from_json(
        self, config_dir: str = "config", config_name: str = "config"
        ) -> dict:
        """
        Получение настроек бота из JSON-файла.

        Данный метод возвращает словарь с настройками бота, взятыми из \
        JSON-файла.

        ### Аргументы:
        - config_name: имя JSON-файла с настройками бота. Имя файла должно быть \
          передано без расширения. Автоматически будет добавлено расширение \
          ".json".
        - config_dir: имя директории с JSON-файлом с настройками бота. \
          По умолчанию это директория "config".

        ### Возращает:
        - dict: словарь с настройками бота, если JSON-файл существует.
        - dict: пустой словарь, если JSON-файл не существует или \
          были переданы некорректные аргументы.

        ### Пример:
        ```python
        from utils.fs.json_manager import JSONManager

        json_manager = JSONManager()
        settings = json_manager.get_bot_settings_from_json("settings")
        print(settings)  # Выведет словарь с настройками бота
        ```
        """

        validate_result = self._validate_get_bot_settings_from_json(
            config_dir, config_name
            )

        if validate_result is not None:
            return {}

        config_path = f"{config_dir}/{config_name}.json"

        if not self.__FS_MANAGER.check_dir_or_file_exists(config_path):
            return {}

        return self.read_json_file(config_path).get("data", {})

    def _validate_content_for_write(self, content: dict) -> None | bool:
        """Проверка данных перед записью в JSON-файл."""

        if not isinstance(content, dict):
            self.logger.error(
                "Должен быть передан словарь, однако был передан %s",
                type(content)
                )
            return False

        return None

    def _validate_get_bot_settings_from_json(
        self, config_dir: str = "config", config_name: str = "config"
        ) -> dict | None:
        """Проверка данных перед получением настроек бота из JSON-файла."""

        if not isinstance(config_dir, str) or not isinstance(config_name, str):
            self.logger.error(
                "Должны быть переданы строки, однако были переданы %s и %s. \
                Возвращен пустой словарь.", type(config_dir), type(config_name)
                )
            return {}

        return None
