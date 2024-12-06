"""Модуль для определения моделей для работы с базой данных.

Этот модуль содержит определения моделей для работы с базой данных в приложении. 
Модели описывают структуру таблиц и их взаимосвязи.

### Модели:
- `User`: Модель для хранения информации о пользователях.
- `Matches`: Модель для хранения информации о матчах между пользователями.


"""

import os
from sqlalchemy import Column, Integer, String, ForeignKey, create_engine
from sqlalchemy.orm import relationship, DeclarativeBase

from dotenv import load_dotenv

load_dotenv()

engine = create_engine(os.getenv("DSN"))


class Base(DeclarativeBase):
    """Базовый класс для определения моделей для работы с базой данных."""
    pass


class User(Base):
    """Модель для хранения информации о пользователях."""

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, nullable=False, unique=True)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    gender = Column(Integer)
    location = Column(String(100))
    profile_url = Column(String(255), nullable=False)

    matches = relationship(
        "Matches", backref="user", cascade="all, delete-orphan"
    )

    def __str__(self) -> str:
        return f"User(id={self.id}, first_name='{self.first_name}')"

    def __repr__(self) -> str:
        return (
            f"<User(id={self.id}, first_name='{self.first_name}', "
            f"last_name='{self.last_name}', age={self.age}, "
            f"gender='{self.gender}', location='{self.location}')>"
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

    user = relationship("User", backref="matches")

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
