"""Менеджер базы данных для работы с пользователями."""

from sqlalchemy.exc import SQLAlchemyError

from db.models.models import User, UserSearchSettings, Session
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
        except SQLAlchemyError as e:
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

    def create_user_search_settings(self, user_id: int, settings_data: dict) \
        -> None:
        """
        Создает настройки пользователя для поиска мэтчей в базе данных.
        
        ### Аргументы:
        - user_id (int): ID пользователя ВКонтакте.
        - settings_data (dict): Словарь с настройками пользователя. \
            Возможные ключи: \
            - age_min (int): Минимальный возраст для поиска \
            - age_max (int): Максимальный возраст для поиска \
            - sex (int): Предпочитаемый пол (0 - любой, 1 - жен., 2 - муж.) \
            - city_id (int): ID города для поиска \
            - city_title (str): Название города для поиска \
            - relation (int): Возрастная группа для поиска
        """
        try:
            if self.get_user_search_settings(user_id):
                self.logger.info(
                    "Настройки для пользователя %d уже существуют. \
                    Создание новых настроек прекращено.",
                    user_id
                )
                return

            settings = UserSearchSettings(user_id=user_id, **settings_data)
            self.__session.add(settings)
            self.__session.commit()

            self.logger.info(
                "Настройки для пользователя %d успешно созданы.", user_id)
        except SQLAlchemyError as e:
            self.__session.rollback()
            self.logger.error(
                "Ошибка при создании настроек пользователя:\n%s", e)
        finally:
            self.__session.close()

    def get_user_search_settings(self, user_id: int) -> UserSearchSettings | None:
        """
        Возвращает настройки пользователя для поиска мэтчей из базы данных.

        ### Аргументы:
        - user_id (int): ID пользователя ВКонтакте.

        ### Возвращает:
        - UserSearchSettings: Объект настроек пользователя для поиска мэтчей.
        - None: Если настройки не были найдены.
        """
        return (
            self.__session
            .query(UserSearchSettings)
            .filter_by(user_id=user_id)
            .first()
        )

    def update_user_settings(self, user_id: int, settings_data: dict) -> None:
        """
        Обновляет настройки пользователя для поиска мэтчей в базе данных.
        
        ### Аргументы:
        - user_id (int): ID пользователя ВКонтакте.
        - settings_data (dict): Словарь с обновляемыми настройками. \
            Возможные ключи: \
            - age_min (int): Минимальный возраст для поиска \
            - age_max (int): Максимальный возраст для поиска \
            - sex (int): Предпочитаемый пол (0 - любой, 1 - жен., 2 - муж.) \
            - city_id (int): ID города для поиска \
            - city_title (str): Название города для поиска \
            - relation (int): Семейное положение.
        """
        try:
            settings = self.get_user_search_settings(user_id)
            if not settings:
                self.create_user_search_settings(user_id, settings_data)
                return

            for key, value in settings_data.items():
                if hasattr(settings, key):
                    setattr(settings, key, value)

            self.__session.commit()
            self.logger.info(
                "Настройки пользователя %d успешно обновлены.", user_id)
        except SQLAlchemyError as e:
            self.__session.rollback()
            self.logger.error(
                "Ошибка при обновлении настроек пользователя:\n%s", e)
        finally:
            self.__session.close()

    def delete_user_settings(self, user_id: int) -> None:
        """Удаляет настройки пользователя для поиска мэтчей из базы данных."""
        try:
            settings = self.get_user_search_settings(user_id)
            if settings:
                self.__session.delete(settings)
                self.__session.commit()
                self.logger.info(
                    "Настройки пользователя %d успешно удалены.", user_id)
        except SQLAlchemyError as e:
            self.__session.rollback()
            self.logger.error(
                "Ошибка при удалении настроек пользователя:\n%s", e)
        finally:
            self.__session.close()
