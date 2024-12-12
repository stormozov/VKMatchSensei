"""Сервис для форматирования."""


class FormatService:
    """Сервис для форматирования."""

    def get_user_vk_link(self, user_id: int) -> str:
        """Получение ссылки на профиль пользователя в VK."""
        return f"https://vk.com/id{user_id}"

    def fmt_user_data_to_db(self, user_data: dict) -> dict:
        """Форматирование пользовательских данных для записи в базу данных."""

        user_vk_link = self.get_user_vk_link(user_data.get("id"))

        user_data["profile_url"] = f"{user_vk_link}"
        user_data["user_id"] = user_data.pop("id")
        user_data["city_id"] = user_data.get("city").get("id")
        user_data["city_title"] = user_data.get("city").get("title")

        user_data.pop("can_access_closed", None)
        user_data.pop("is_closed", None)
        user_data.pop("city", None)

        return user_data
