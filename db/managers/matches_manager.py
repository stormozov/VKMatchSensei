"""Менеджер базы данных для работы с мэтчей."""

from sqlalchemy.exc import SQLAlchemyError

from db.models.models import Matches, Session
from services.formatters.matches_formatter import format_matches
from services.formatters.module_formatters import get_module_part
from utils.logging.setup import setup_logger


class DatabaseMatchesManager:
    """Менеджер базы данных для работы с мэтчами."""

    __session = Session()

    def __init__(self) -> None:
        self.logger = setup_logger(
            module_name=get_module_part(__name__, idx=0),
            logger_name=__name__
        )

    def save_user_match(self, user_id: int, matches: list[dict]) -> None:
        """Сохраняет информацию о мэтче пользователя в базу данных."""
        try:
            saved_count = 0
            for match in matches:
                match = format_matches(match)
                new_match = Matches(user_id=user_id, **match)
                if not self.get_user_matches(user_id, match):
                    self.__session.add(new_match)
                    saved_count += 1
                else:
                    self.logger.debug(
                        "Мэтч %s уже существует для пользователя %d",
                        match.get("match_id"), user_id
                    )

            if saved_count > 0:
                self.__session.commit()
                self.logger.info(
                    "Сохранено %d новых мэтчей для пользователя %d",
                    saved_count, user_id
                )
            else:
                self.logger.info(
                    "Новых мэтчей для сохранения не найдено для пользователя %d",
                    user_id
                )
        except SQLAlchemyError as e:
            self.__session.rollback()
            self.logger.error("Ошибка при сохранении мэтча:\n%s", e)
        finally:
            self.__session.close()

    def get_user_matches(self, user_id: int, matches: dict = None) \
        -> list[Matches]:
        """Возвращает список мэтчей пользователя из базы данных.
        
        ### Аргументы:
        - user_id (int): ID пользователя
        - matches (dict, optional): Словарь с параметрами для фильтрации. \
          Если не указан, возвращает все мэтчи пользователя.
        """

        if not isinstance(user_id, int) or user_id < 0:
            return []

        try:
            query = self.__session.query(Matches).filter_by(user_id=user_id)

            if matches and isinstance(matches, dict):
                query = query.filter_by(**matches)
                result = query.first()
                return [result] if result else []

            return query.all() or []
        except SQLAlchemyError as e:
            self.logger.error(
                "Ошибка при получении мэтчей для пользователя %d: %s",
                user_id, str(e)
            )
            return []
