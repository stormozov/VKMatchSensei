"""Обработка команды поиска."""

from config.bot_config import MESSAGES_CONFIG
from db.managers.matches_manager import DatabaseMatchesManager
from db.managers.user_manager import DatabaseUserManager
from db.models.models import UserSearchSettings
from services.formatters.module_formatters import get_module_part
from services.vk_api.msg_service import MessageService
from services.vk_api.vk_api_service import VKApiService
from utils.logging.setup import setup_logger

vk_service = VKApiService()

logger = setup_logger(
    module_name=get_module_part(__name__, idx=0), logger_name=__name__
)


class SearchHandler:
    """Обработка команды поиска."""

    __msg_service = MessageService()

    def start_searching(self, user_id: int) -> None:
        """Обработка команды поиска."""

        self.__msg_service.send_message(
            user_id,
            msg=MESSAGES_CONFIG.get(
                "start_searching_matches", MESSAGES_CONFIG.get("error")
            )
        )

        db_user_manager = DatabaseUserManager()
        search_settings = db_user_manager.get_user_search_settings(user_id)

        group_info = self.search_group_handler(search_settings)
        group_members = self.search_user_group_handler(group_info)
        matches = self.search_result_handler(
            group_members, search_settings, group_info
        )

        self.load_matches_to_db(user_id, matches)

        self.__msg_service.send_message(
            user_id,
            msg=MESSAGES_CONFIG.get(
                "end_searching_matches", MESSAGES_CONFIG.get("error")
            )
        )

    def search_group_handler(self, search_settings: UserSearchSettings) \
        -> list[dict]:
        """Обработка команды поиска групп."""
        return vk_service.get_group_info(
            search_settings.city_id, search_settings.city_title
        )

    def search_user_group_handler(self, group_info: list[dict], offset: int = 0) \
        -> list[dict]:
        """Обработка команды поиска групп пользователя."""
        group_id = group_info[0].get("id")
        return vk_service.get_group_members(group_id, offset)

    def search_result_handler(
        self,
        group_members: list[dict],
        search_settings: UserSearchSettings,
        group_info: list
        ) -> list:
        """Обработка команды поиска результата."""

        offset = 0

        logger.info(
            "Всего было найдено %d пользователей в группе.", len(group_members)
        )

        filtered_members = self.is_preferred_gender(
            group_members, search_settings
        )
        filtered_members = self.is_in_preferred_city(
            filtered_members, search_settings
        )
        filtered_members = self.can_send_message(filtered_members)

        logger.info(
            "Отфильтровано %d пользователей, удовлетворяющих условиям поиска.",
            len(filtered_members)
        )

        while len(filtered_members) < 25:
            logger.info(
                "Найдено менее 25 пользователей, выполняется новый поиск..."
            )
            group_members = self.search_user_group_handler(group_info, offset)
            logger.info(
                "Всего было найдено %d пользователей в группе.",
                len(group_members)
            )

            filtered_members += self.is_preferred_gender(
                group_members, search_settings
            )
            filtered_members = self.is_in_preferred_city(
                filtered_members, search_settings
            )
            filtered_members = self.can_send_message(filtered_members)

            logger.info(
                "Отфильтровано %d пользователей, удовлетворяющих условиям поиска.",
                len(filtered_members)
            )

            offset += len(group_members)

            if len(group_members) < 1000:
                logger.info("Достигнут конец списка участников группы.")
                break

        return filtered_members

    def is_preferred_gender(
        self,
        members: list[dict],
        search_settings: UserSearchSettings
        ) -> list:
        """Проверка предпочитаемого пола."""
        return [
            member
            for member in members
            if member.get("sex") == search_settings.sex
        ]

    def is_in_preferred_city(
        self,
        members: list[dict],
        search_settings: UserSearchSettings
        ) -> list[dict]:
        """Проверка вхождения в предпочитаемый город."""
        return [
            member
            for member in members
            if member.get("city", {}).get("id", 0) == search_settings.city_id
        ]

    def load_matches_to_db(self, user_id: int, matches: list[dict]) -> None:
        """Загрузка найденных мэтчей в базу данных."""
        DatabaseMatchesManager().save_user_match(user_id, matches)

    def is_within_age_range(self, member, search_settings) -> bool:
        """Проверка возраста."""

    def can_send_message(self, group_members: list[dict]) -> bool:
        """Проверка возможности отправки сообщения."""
        return [
            member
            for member in group_members
            if member.get("can_write_private_message", 0) == 1
        ]
