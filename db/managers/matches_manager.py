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
            for match in matches:
                match = format_matches(match)
                new_match = Matches(user_id=user_id, **match)
                if self.get_user_matches(user_id, match) is None:
                    self.__session.add(new_match)
            self.__session.commit()
            self.logger.info("Мэтчи пользователя %d успешно сохранены.", user_id)
        except SQLAlchemyError as e:
            self.__session.rollback()
            self.logger.error("Ошибка при сохранении мэтча:\n%s", e)
        finally:
            self.__session.close()

    def get_user_matches(self, user_id: int, matches: dict) \
        -> list[Matches] | None:
        """Возвращает список мэтчей пользователя из базы данных."""

        if not isinstance(user_id, int) or user_id < 0:
            return []

        if not isinstance(matches, dict):
            return []

        return (
            self.__session
            .query(Matches)
            .filter_by(user_id=user_id, **matches)
            .first()
        )
