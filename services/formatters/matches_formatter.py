"""Форматирование данных мэтчей для записи в базу данных."""

from services.formatters.db_user_formatter import DatabaseUserFormatServices


def format_matches(match: dict) -> dict:
    """Форматирует список мэтчей для записи в базу данных."""

    user_formatter = DatabaseUserFormatServices()

    return {
        "match_id": match.get("id", 0),
        "first_name": match.get("first_name", ""),
        "last_name": match.get("last_name", ""),
        "profile_url": user_formatter.get_user_vk_link(match.get("id")),
    }
