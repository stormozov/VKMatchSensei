"""Менеджер базы данных для работы с пользователями."""

from db.models.models import User, Session
from services.formatters.db_user_formatter import DatabaseUserFormatServices
from services.formatters.module_formatters import get_module_part
from utils.logging.setup import setup_logger


class DatabaseUserManager:
    """Менеджер базы данных для работы с пользователями."""

    __fmt_service = DatabaseUserFormatServices()
    __session = Session()

    def __init__(self) -> None:
        self.logger = setup_logger(
            module_name=get_module_part(__name__, idx=0),
            logger_name=__name__
            )

    def create_user(self, data: dict) -> None:
        """Создает пользователя в базе данных."""

        try:
            new_user = User(**self.__fmt_service.fmt_user_data_to_db(data))

            if self.get_user_by_id(new_user.user_id):
                return

            self.__session.add(new_user)
            self.__session.commit()

            self.logger.info(
                'Пользователь "%s" успешно создан.', new_user.profile_url)
        except Exception as e:
            self.__session.rollback()
            self.logger.error("Ошибка при создании пользователя:\n%s", e)
        finally:
            self.__session.close()

    def get_user_by_id(self, user_id: int) -> User | None:
        """Возвращает пользователя по его id."""
        return self.__session.query(User).filter_by(user_id=user_id).first()

    def update_user(self, user_id: int) -> None:
        """Обновляет данные пользователя в базе данных."""

    def delete_user(self, user_id: int) -> None:
        """Удаляет пользователя из базы данных."""
