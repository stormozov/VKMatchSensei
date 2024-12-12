"""Менеджер базы данных для работы с пользователями."""

from db.models.models import User, Session
from services.fmt_service import FormatService
from utils.fs.name_fmt import get_module_part
from utils.logging.setup import setup_logger

logger = setup_logger(get_module_part(__name__, idx=0), logger_name=__name__)


class DatabaseUserManager:
    """Менеджер базы данных для работы с пользователями."""

    fmt_service = FormatService()
    session = Session()

    def create_user(self, data: dict) -> None:
        """Создает пользователя в базе данных."""

        try:
            new_user = User(**self.fmt_service.fmt_user_data_to_db(data))

            if self.get_user_by_id(new_user.user_id): return

            self.session.add(new_user)
            self.session.commit()
            logger.info(
                f'Пользователь "{new_user.profile_url}" успешно создан.')
        except Exception as e:
            self.session.rollback()
            logger.error(f"Ошибка при создании пользователя:\n{e}")
        finally:
            self.session.close()

    def get_user_by_id(self, user_id: int) -> User | None:
        """Возвращает пользователя по его id."""
        return self.session.query(User).filter_by(user_id=user_id).first()

    def update_user(self, user_id: int) -> None:
        """Обновляет данные пользователя в базе данных."""
        pass

    def delete_user(self, user_id: int) -> None:
        """Удаляет пользователя из базы данных."""
        pass
