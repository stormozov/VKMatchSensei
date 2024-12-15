"""Обработчики базовых команд бота."""

from config.bot_config import KEYBOARD_CONFIG, MESSAGES_CONFIG
from db.managers.user_manager import DatabaseUserManager
from services.vk_service import VKApiService

vk_service = VKApiService()
db_user_manager = DatabaseUserManager()


class BasicHandler:
    """Обработчик базовых команд бота."""

    def start_handler(self, user_id: int, send_message: object) -> None:
        """Обработчик команды "/start"."""

        # Отправка сообщения пользователю в чате.
        send_message(
            user_id,
            msg=MESSAGES_CONFIG.get("start", ""),
            btns=KEYBOARD_CONFIG.get("start", {}),
            )

        # Получение информации о пользователе по его ID.
        fetched_user_data: dict = vk_service.get_user_info(user_id)

        # Загрузка данных пользователя в базу данных.
        db_user_manager.create_user(fetched_user_data)

        # Поиск пользователей по заданным параметрам.
        # TODO: Реализовать поиск пользователей по заданным параметрам.

        # Форматирование результата поиска пользователей.
        # TODO: Реализовать форматирование результата поиска пользователей.

        # Загрузка найденных данных мэтчей в базу данных.
        # TODO: Реализовать загрузку данных мэтчей в базу данных.
