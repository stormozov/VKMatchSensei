"""Форматирование данных мэтчей для записи в базу данных."""

import time

from services.formatters.db_user_formatter import DatabaseUserFormatServices
from services.vk_api.vk_api_service import VKApiService


def format_matches(match: dict[str, str | int]) -> dict:
    """Форматирует список мэтчей для записи в базу данных."""

    user_formatter = DatabaseUserFormatServices()
    vk_api_service = VKApiService()
    match_vk_id = match.get("id")
    photo_id = 0

    if match.get("is_closed") is False:
        photo_id = (
            vk_api_service
            .get_user_photos(match_vk_id, rev=1)
            .get("items", [{"id": 0}])[0]
            .get("id", 0)
        )

    time.sleep(1)

    return {
        "match_id": match_vk_id,
        "first_name": match.get("first_name", ""),
        "last_name": match.get("last_name", ""),
        "profile_url": user_formatter.get_user_vk_link(match_vk_id),
        "photo_id": photo_id if photo_id != 0 else None,
    }
