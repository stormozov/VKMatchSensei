"""Модуль для менеджера управления схемой базы данных."""

from db.models.models import Base, engine


class DatabaseSchemaManager:
    """
    Менеджер для управления схемой базы данных.
    
    ### Методы:
    - `create_tables()`: Метод для создания всех таблиц в базе данных.
    - `drop_tables_cascade()`: Метод для удаления всех таблиц в базе данных.
    - `recreate_tables()`: Метод для перезаписи всех таблиц в базе данных.
    """

    def create_tables(self):
        """Создает все таблицы в БД, описанные в моделях."""
        try:
            Base.metadata.create_all(engine)
        except Exception as e:
            print("Ошибка при создании таблиц:", e)

    def drop_tables_cascade(self):
        """
        Каскадно удаляет все таблицы из БД независимо от наличия в них данных.
        """
        try:
            Base.metadata.drop_all(engine)
        except Exception as e:
            print("Ошибка при удалении таблиц:", e)

    def recreate_tables(self):
        """
        Перезаписывает все таблицы в БД независимо от наличия в них данных.
        
        ### Примечание:
        - Не рекомендуется использовать в продакшене. Все данные в таблицах 
          при перезаписи будут потеряны.
        """

        self.drop_tables_cascade()
        self.create_tables()
