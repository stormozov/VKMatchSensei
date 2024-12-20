"""Модуль для определения моделей для работы с базой данных.

Этот модуль содержит определения моделей для работы с базой данных в 
приложении. Модели описывают структуру таблиц и их взаимосвязи.

### Модели:
- `User`: Модель для хранения информации о пользователях.
- `UserSettings`: Модель для хранения настроек пользователя.
- `Matches`: Модель для хранения информации о матчах между пользователями.

### Дополнительно определены следующие объекты:
- `engine`: Объект для подключения к базе данных.
- `Session`: Класс для работы с сессиями базы данных.
- `Base`: Базовый класс для определения моделей для работы с базой данных.
"""

import os
from sqlalchemy import (
    Column, Integer, SmallInteger, String, ForeignKey, create_engine
)
from sqlalchemy.orm import relationship, DeclarativeBase, sessionmaker

from dotenv import load_dotenv

load_dotenv()

engine = create_engine(os.getenv("DSN"))
Session = sessionmaker(bind=engine)


class Base(DeclarativeBase):
    """Базовый класс для определения моделей для работы с базой данных."""


class User(Base):
    """Модель для хранения информации о пользователях."""

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, nullable=False, unique=True)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    sex = Column(Integer)
    city_id = Column(SmallInteger)
    city_title = Column(String(100))
    profile_url = Column(String(255), nullable=False)

    matches = relationship(
        "Matches", back_populates="user", cascade="all, delete-orphan"
    )
    settings = relationship(
        "UserSearchSettings",
        back_populates="user",
        uselist=False,
        cascade="all, delete-orphan"
    )

    def __str__(self) -> str:
        return f"User(id={self.id}, first_name='{self.first_name}')"

    def __repr__(self) -> str:
        return (
            f"<User(id={self.id}, first_name='{self.first_name}', "
            f"last_name='{self.last_name}', sex={self.sex}, "
            f"city_title='{self.city_title}')>"
        )


class UserSearchSettings(Base):
    """Модель для хранения настроек пользователя для поиска мэтчей.
    
    ### Атрибуты:
    - id (int): Уникальный идентификатор записи.
    - user_id (int): Внешний ключ, ссылающийся на пользователя.
    - age_min (int): Минимальный возраст для поиска (по умолчанию 18).
    - age_max (int): Максимальный возраст для поиска (по умолчанию 99).
    - sex (int): Предпочитаемый пол (0 - любой, 1 - женский, 2 - мужской).
    - city_id (int): ID города для поиска (по умолчанию 1).
    - city_title (str): Название города для поиска (по умолчанию "Москва").
    - relation (int): Семейное положение (по умолчанию 0 - не указано).

    ### Отношения:
    - user (User): Объект пользователя, которому принадлежат настройки.
    """

    __tablename__ = "user_settings"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(
        Integer,
        ForeignKey("users.user_id"),
        nullable=False,
        unique=True
    )
    age_min = Column(SmallInteger, nullable=False, default=18)
    age_max = Column(SmallInteger, nullable=False, default=99)
    sex = Column(SmallInteger, default=0)
    city_id = Column(SmallInteger, default=1)
    city_title = Column(String(100), default="Москва")
    relation = Column(SmallInteger, default=0)

    user = relationship("User", back_populates="settings")

    def __str__(self) -> str:
        return f"UserSettings(id={self.id}, user_id={self.user_id})"

    def __repr__(self) -> str:
        return (
            f"<UserSettings(id={self.id}, user_id={self.user_id}, "
            f"age_min={self.age_min}, age_max={self.age_max}, "
            f"sex={self.sex}, city_title='{self.city_title}')>"
        )


class Matches(Base):
    """Модель для хранения информации о мэтчах."""

    __tablename__ = "matches"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    match_id = Column(Integer, nullable=False)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    profile_url = Column(String(255), nullable=False)
    photo = Column(String(255))

    user = relationship("User", back_populates="matches")

    def __str__(self) -> str:
        return (
            f"Matches(id={self.id}, user_id={self.user_id}, "
            f"match_id={self.match_id}, first_name='{self.first_name}')"
        )

    def __repr__(self) -> str:
        return (
            f"<Matches(id={self.id}, user_id={self.user_id}, "
            f"match_id={self.match_id}, first_name='{self.first_name}', "
            f"last_name='{self.last_name}', profile_url='{self.profile_url}')>"
        )
