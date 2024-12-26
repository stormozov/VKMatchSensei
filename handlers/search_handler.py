"""Обработка команды поиска."""

import copy
from config.bot_config import KEYBOARD_CONFIG, MESSAGES_CONFIG
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
        group_info: list[dict]
        ) -> list[dict]:
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

    def show_matches(self, user_id: int, match_index: int = 0) -> None:
        """Показывает найденные мэтчи пользователя по одному."""

        matches_manager = DatabaseMatchesManager()
        matches = matches_manager.get_user_matches(user_id)
        attachment = None

        logger.info(
            "Получено %d мэтчей для пользователя %d",
            len(matches) if matches else 0, user_id
        )

        if not matches:
            self.__msg_service.send_message(
                user_id,
                msg=MESSAGES_CONFIG.get(
                    "no_matches_found", MESSAGES_CONFIG.get("error")
                ),
                btns=KEYBOARD_CONFIG["main_menu"]
            )
            return

        # Проверяем валидность индекса
        if match_index >= len(matches):
            logger.info(
                "Индекс %d превышает количество мэтчей, сброс на начало",
                match_index
            )
            match_index = 0

        if match_index == 0:
            self.__msg_service.send_message(
                user_id,
                msg=MESSAGES_CONFIG.get(
                    "show_matches_start", MESSAGES_CONFIG.get("error")
                ) % len(matches)
            )

        current_match = matches[match_index]
        match_msg = MESSAGES_CONFIG.get(
            "show_match_template", MESSAGES_CONFIG.get("error")
        ).format(
            first_name=current_match.first_name,
            last_name=current_match.last_name,
            profile_url=current_match.profile_url
        )

        if current_match.photo_id:
            attachment = f"photo{current_match.match_id}_{current_match.photo_id}"

        # Определяем какую клавиатуру показывать
        keyboard_name = (
            "match_navigation"
            if match_index < len(matches) - 1
            else "main_menu"
        )
        logger.info(
            "Используется клавиатура %s для индекса %d из %d", 
            keyboard_name, match_index, len(matches)
        )

        keyboard = copy.deepcopy(KEYBOARD_CONFIG[keyboard_name])
        if keyboard_name == "match_navigation":
            # Форматируем payload для следующего индекса
            keyboard["actions"][0]["payload"] = (
                keyboard["actions"][0]["payload"] % (match_index + 1)
            )

        self.__msg_service.send_message(
            user_id,
            msg=match_msg,
            btns=keyboard,
            attachment=attachment
        )
