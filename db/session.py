"""Модуль для создания сессии для работы с базой данных."""

from sqlalchemy.orm import sessionmaker

from db.models.models import engine


def create_session() -> None:
    """Создание сессии для работы с базой данных."""
    return sessionmaker(bind=engine)
