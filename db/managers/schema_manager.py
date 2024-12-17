"""Модуль для менеджера управления схемой базы данных."""

from db.models.models import Base, engine
from services.formatters.module_formatters import get_module_part
from utils.logging.setup import setup_logger


class DatabaseSchemaManager:
    """
    Менеджер для управления схемой базы данных.
    
    ### Методы:
    - `create_tables()`: Метод для создания всех таблиц в базе данных.
    - `drop_tables_cascade()`: Метод для удаления всех таблиц в базе данных.
    - `recreate_tables()`: Метод для перезаписи всех таблиц в базе данных.
    """

    def __init__(self) -> None:
        self.logger = setup_logger(
            module_name=get_module_part(__name__, idx=0),
            logger_name=__name__
            )

    def create_tables(self) -> None:
        """Создает все таблицы в БД, описанные в моделях."""
        try:
            Base.metadata.create_all(engine)
            self.logger.info("Таблицы успешно созданы.")
        except Exception as e:
            self.logger.error("Ошибка при создании таблиц:\n%s", e)

    def drop_tables_cascade(self) -> None:
        """
        Каскадно удаляет все таблицы из БД независимо от наличия в них данных.
        """
        try:
            Base.metadata.drop_all(engine)
            self.logger.info("Таблицы успешно удалены.")
        except Exception as e:
            self.logger.error("Ошибка при удалении таблиц:\n%s", e)

    def recreate_tables(self) -> None:
        """
        Перезаписывает все таблицы в БД независимо от наличия в них данных.
        
        ### Примечание:
        - Не рекомендуется использовать в продакшене. Все данные в таблицах 
          при перезаписи будут потеряны.
        """

        self.logger.info("Начинаю перезапись таблиц...")
        self.drop_tables_cascade()
        self.create_tables()
        self.logger.info("Таблицы успешно перезаписаны.")
