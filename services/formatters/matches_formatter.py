"""Форматирование данных мэтчей для записи в базу данных."""

import time

from services.formatters.db_user_formatter import DatabaseUserFormatServices
from services.vk_api.vk_api_service import VKApiService


class MatchFormatter:
    """Класс для форматирования мэтчей для записи в базу данных."""

    def __init__(self, match: dict[str, str | int]):
        self.match = match
        self.user_formatter = DatabaseUserFormatServices()
        self.vk_api_service = VKApiService()

    def format(self) -> dict:
        """Форматирует мэтч для записи в базу данных."""

        match_vk_id = self.match.get("id")
        photo_id = self.get_photo_id_if_open(
            match_vk_id, self.match.get("is_closed")
        )

        return self.create_formatted_match_dict(match_vk_id, photo_id)

    def get_photo_id_if_open(self, match_vk_id: int, is_closed: bool) \
        -> int | None:
        """Получает ID фотографии, если профиль не закрыт."""

        if is_closed:
            return None

        time.sleep(1) # Пауза в 1 секунду, чтобы избежать ограничений API ВК.

        photo_data = self.vk_api_service.get_user_photos(match_vk_id, rev=1)
        return photo_data.get("items", [{"id": None}])[0].get("id")

    def create_formatted_match_dict(
        self, match_vk_id: int, photo_id: int | None
        ) -> dict:
        """Создает отформатированный словарь для мэтча."""
        return {
            "match_id": match_vk_id,
            "first_name": self.match.get("first_name", ""),
            "last_name": self.match.get("last_name", ""),
            "profile_url": self.user_formatter.get_user_vk_link(match_vk_id),
            "photo_id": photo_id,
        }


def format_matches(match: dict[str, str | int]) -> dict:
    """Форматирует список мэтчей для записи в базу данных."""
    return MatchFormatter(match).format() if match else {}
