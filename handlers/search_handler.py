"""Обработка команды поиска."""

import copy
import json

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
        return vk_service.get_group_members(group_info[0].get("id"), offset)

    def search_result_handler(
        self,
        group_members: list[dict],
        search_settings: UserSearchSettings,
        group_info: list[dict]
    ) -> list[dict]:
        """Обработка команды поиска результата."""

        logger.info(
            "Всего было найдено %d пользователей в группе.", len(group_members)
        )

        filtered_members = self.filter_members(group_members, search_settings)

        logger.info(
            "Отфильтровано %d пользователей, удовлетворяющих условиям поиска.",
            len(filtered_members)
        )

        filtered_members = self.fetch_additional_members(
            group_info,
            search_settings,
            filtered_members,
            0
        )

        return filtered_members

    def show_matches(self, user_id: int, match_index: int = 0) -> None:
        """Показывает найденные мэтчи пользователя по одному."""

        matches = self.get_user_matches(user_id)
        if not matches:
            self.handle_no_matches(user_id)
            return

        match_index = self.validate_match_index(match_index, len(matches))
        if match_index == 0:
            self.send_start_message(user_id, len(matches))

        match_msg, attachment = self.format_match_message(matches[match_index])

        keyboard = self.get_keyboard_for_match_navigation(
            match_index, len(matches)
        )

        self.__msg_service.send_message(
            user_id,
            msg=match_msg,
            btns=keyboard,
            attachment=attachment
        )

    def filter_members(
        self,
        group_members: list[dict],
        search_settings: UserSearchSettings
    ) -> list[dict]:
        """Фильтрует участников на основе настроек поиска."""
        return [
            member for member in group_members
            if self.is_member_matching(member, search_settings)
        ]

    def fetch_additional_members(
        self,
        group_info: list[dict],
        search_settings: UserSearchSettings,
        filtered_members: list[dict],
        offset: int
    ) -> list[dict]:
        """Получает дополнительных участников, если найдено менее 25."""
        while len(filtered_members) < 25:
            logger.info(
                "Найдено менее 25 пользователей, выполняется новый поиск..."
            )
            group_members = self.search_user_group_handler(group_info, offset)
            logger.info(
                "Всего было найдено %d пользователей в группе.",
                len(group_members)
            )

            filtered_members.extend(self.filter_members(
                group_members, search_settings
            ))

            logger.info(
                "Отфильтровано %d пользователей, удовлетворяющих условиям поиска.",
                len(filtered_members)
            )

            offset += len(group_members)

            if len(group_members) < 1000:
                logger.info("Достигнут конец списка участников группы.")
                break

        return filtered_members

    @staticmethod
    def is_member_matching(member: dict, search_settings: UserSearchSettings) \
        -> bool:
        """Проверяет, соответствует ли участник критериям поиска."""
        return (
            member.get("sex") == search_settings.sex
            and member.get("city", {}).get("id", 0) == search_settings.city_id
            and member.get("can_write_private_message", 0) == 1
        )

    def load_matches_to_db(self, user_id: int, matches: list[dict]) -> None:
        """Загрузка найденных мэтчей в базу данных."""
        DatabaseMatchesManager().save_user_match(user_id, matches)

    def is_within_age_range(self, member, search_settings) -> bool:
        """Проверка возраста."""

    def get_user_matches(self, user_id: int) -> list:
        """Получает мэтчи пользователя из базы данных."""
        matches_manager = DatabaseMatchesManager()
        return matches_manager.get_user_matches(user_id)

    def handle_no_matches(self, user_id: int) -> None:
        """Обрабатывает случай, когда нет найденных мэтчей."""
        self.__msg_service.send_message(
            user_id,
            msg=MESSAGES_CONFIG.get(
                "no_matches_found", MESSAGES_CONFIG.get("error")
            ),
            btns=KEYBOARD_CONFIG["main_menu"]
        )

    def validate_match_index(self, match_index: int, total_matches: int) -> int:
        """Проверяет валидность индекса мэтча."""
        if match_index >= total_matches:
            logger.info(
                "Индекс %d превышает количество мэтчей, сброс на начало",
                match_index
            )
            return 0
        return match_index

    def send_start_message(self, user_id: int, total_matches: int) -> None:
        """Отправляет сообщение о начале показа мэтчей."""
        self.__msg_service.send_message(
            user_id,
            msg=MESSAGES_CONFIG.get(
                "show_matches_start", MESSAGES_CONFIG.get("error")
            ) % total_matches
        )

    def format_match_message(self, current_match) -> tuple:
        """Форматирует сообщение о текущем мэтче."""

        match_msg = MESSAGES_CONFIG.get(
            "show_match_template", MESSAGES_CONFIG.get("error")
        ).format(
            first_name=current_match.first_name,
            last_name=current_match.last_name,
            profile_url=current_match.profile_url
        )

        attachment = (
            f"photo{current_match.match_id}_{current_match.photo_id}"
            if current_match.photo_id
            else None
        )

        return match_msg, attachment

    def get_keyboard_for_match_navigation(
        self, match_index: int, total_matches: int
        ) -> dict:
        """Определяет, какую клавиатуру показывать."""

        keyboard_name = (
            "match_navigation"
            if match_index < total_matches - 1
            else "main_menu"
        )
        logger.info(
            "Используется клавиатура %s для индекса %d из %d", 
            keyboard_name, match_index, total_matches
        )

        keyboard = copy.deepcopy(KEYBOARD_CONFIG[keyboard_name])
        if keyboard_name == "match_navigation":
            # Форматируем payload для следующего индекса
            keyboard["actions"][0]["payload"] = (
                keyboard["actions"][0]["payload"] % match_index
            )

        return keyboard

    def handle_next_match(self, user_id: int, event) -> None:
        """Обработка команды показа следующего мэтча."""

        payload_str = getattr(event, 'payload', None)
        if payload_str:
            try:
                payload = json.loads(payload_str)
                logger.info("Получен payload: %s", payload)
                current_index = int(payload.get('match_index', 0))
                next_index = current_index + 1
                self.show_matches(user_id, next_index)
            except (json.JSONDecodeError, ValueError) as e:
                logger.error("Ошибка при обработке payload: %s", str(e))
                self.__msg_service.send_message(
                    user_id,
                    msg=MESSAGES_CONFIG.get(
                        "unknown_command", MESSAGES_CONFIG.get("error")
                    ),
                    btns=KEYBOARD_CONFIG.get("main_menu"),
                )
        else:
            self.show_matches(user_id)
