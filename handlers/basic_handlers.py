"""Обработчики базовых команд бота."""

from config.bot_config import KEYBOARD_CONFIG, MESSAGES_CONFIG
from db.managers.user_manager import DatabaseUserManager
from services.vk_api.msg_service import MessageService
from services.vk_api.vk_api_service import VKApiService
from handlers.search_settings_handler import SearchSettingsHandler

vk_service = VKApiService()
db_user_manager = DatabaseUserManager()


class BasicHandler:
    """Обработчик базовых команд бота."""

    def __init__(self):
        self.__msg_service = MessageService()
        self.__search_handler = SearchSettingsHandler()

    def start_handler(self, user_id: int) -> None:
        """Обработчик команды "/start"."""

        # Отправка сообщения пользователю в чате.
        self.__msg_service.send_message(
            user_id,
            msg=MESSAGES_CONFIG.get("start", MESSAGES_CONFIG.get("error")),
            btns=KEYBOARD_CONFIG.get("start", None),
        )

        # Получение информации о пользователе по его ID.
        fetched_user_data: dict = vk_service.get_user_info(user_id)

        # Загрузка данных пользователя в базу данных.
        db_user_manager.create_user(fetched_user_data)

    def is_in_search_settings(self, user_id: int) -> bool:
        """Проверяет, находится ли пользователь в процессе настройки поиска."""
        return self.__search_handler.is_in_search_settings(user_id)

    def handle_unknown_message(self, user_id: int) -> None:
        """Обработка неизвестных сообщений."""
        self.__msg_service.send_message(
            user_id,
            msg=MESSAGES_CONFIG.get(
                "unknown_command", MESSAGES_CONFIG.get("error")
            ),
            btns=KEYBOARD_CONFIG.get("start", None),
        )

    def search_settings_handler(self, request: str, user_id: int) -> None:
        """Обработчик настройки поиска."""
        self.__search_handler.handle_search_settings(request, user_id)
