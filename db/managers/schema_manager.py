"""Модуль для менеджера управления схемой базы данных."""

from db.models.models import Base, engine
from utils.fs.name_fmt import get_module_part
from utils.logging.setup import setup_logger

logger = setup_logger(get_module_part(__name__, idx=0), logger_name=__name__)


class DatabaseSchemaManager:
    """
    Менеджер для управления схемой базы данных.
    
    ### Методы:
    - `create_tables()`: Метод для создания всех таблиц в базе данных.
    - `drop_tables_cascade()`: Метод для удаления всех таблиц в базе данных.
    - `recreate_tables()`: Метод для перезаписи всех таблиц в базе данных.
    """

    def create_tables(self) -> None:
        """Создает все таблицы в БД, описанные в моделях."""
        try:
            Base.metadata.create_all(engine)
            logger.info("Таблицы успешно созданы.")
        except Exception as e:
            logger.error(f"Ошибка при создании таблиц:\n{e}")

    def drop_tables_cascade(self) -> None:
        """
        Каскадно удаляет все таблицы из БД независимо от наличия в них данных.
        """
        try:
            Base.metadata.drop_all(engine)
            logger.info("Таблицы успешно удалены.")
        except Exception as e:
            logger.error(f"Ошибка при удалении таблиц:\n{e}")

    def recreate_tables(self) -> None:
        """
        Перезаписывает все таблицы в БД независимо от наличия в них данных.
        
        ### Примечание:
        - Не рекомендуется использовать в продакшене. Все данные в таблицах 
          при перезаписи будут потеряны.
        """

        logger.info("Начинаю перезапись таблиц...")
        self.drop_tables_cascade()
        self.create_tables()
        logger.info("Таблицы успешно перезаписаны.")
