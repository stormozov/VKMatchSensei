"""Менеджер для работы с JSON-файлами."""

import os
import json

from utils.fs.fs_manager import FileSystemManager
from utils.fs.name_fmt import get_module_part
from utils.logging.setup import setup_logger

logger = setup_logger(get_module_part(__name__), logger_name=__name__)


class JSONManager:
    """
    Менеджер для работы с JSON-файлами.

    ### Основные методы:
    - `write_json_file`: Запись JSON-файла.
    - `read_json_file`: Чтение JSON-файла и получение его содержимого в формате
      словаря.
    - `delete_json_file`: Удаление JSON-файла.
    - `check_json_file_exists`: Проверка существования JSON-файла.
    - `get_bot_settings_from_json`: Получение настроек бота из JSON-файла.
    """

    __DEFAULT_ENCODING = "utf-8"
    __FS_MANAGER = FileSystemManager()

    def write_json_file(self, file_path: str, data: dict) -> None:
        """
        Запись JSON-файла.
        
        Формат передаваемого пути должен быть "utils/timetools/tools" для 
        директории или "utils/timetools/tools/file.log" для файла.
        """

        if self.__validate_data_for_write(data):
            return None

        file_path = self.__FS_MANAGER.get_full_path(file_path)

        if not self.__FS_MANAGER.check_dir_or_file_exists(file_path):
            return None

        with open(file_path, "w", encoding=self.__DEFAULT_ENCODING) as file:
            json.dump(data, file)

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

        Данный метод возвращает словарь с настройками бота, взятыми из
        JSON-файла.

        ### Аргументы:
        - config_name: имя JSON-файла с настройками бота. Имя файла должно быть
          передано без расширения. Автоматически будет добавлено расширение 
          ".json".
        - config_dir: имя директории с JSON-файлом с настройками бота.
          По умолчанию это директория "config".

        ### Возращает:
        - dict: словарь с настройками бота, если JSON-файл существует.
        - dict: пустой словарь, если JSON-файл не существует.

        ### Пример:
        ```python
        from utils.fs.json_manager import JSONManager

        json_manager = JSONManager()
        settings = json_manager.get_bot_settings_from_json("settings")
        print(settings)  # Выведет словарь с настройками бота
        ```
        """

        config_path = f"{config_dir}/{config_name}.json"

        if not self.__FS_MANAGER.check_dir_or_file_exists(config_path):
            return {}

        return self.read_json_file(config_path).get("data", {})

    def __validate_data_for_write(self, data: dict) -> bool:
        """Проверка данных перед записью в JSON-файл."""

        if not isinstance(data, dict):
            logger.error(
                "Должен быть передан словарь, однако был передан %s",
                type(data)
                )
            return True

        if not data:
            logger.error(
                "Должен быть передан словарь с данными, "
                "однако был передан пустой словарь"
                )
            return True

        return False
