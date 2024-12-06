"""Модуль для создания таблиц в базе данных."""

from db.managers.schema import DatabaseSchemaManager


if __name__ == "__main__":
    schema_manager = DatabaseSchemaManager()
    schema_manager.recreate_tables()
