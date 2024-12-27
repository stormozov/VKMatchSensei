"""Сервис для работы с API ВКонтакте"""

import os
import requests

from dotenv import load_dotenv
from services.formatters.module_formatters import get_module_part
from utils.logging.setup import setup_logger

load_dotenv()


class VKAPIError(Exception):
    """Базовый класс для исключений VK API."""


class VKAPIAuthError(VKAPIError):
    """Исключение при авторизации VK API."""


class VKApiService:
    """
    Сервис для работы с API ВКонтакте.
    
    Содержит различные методы для взаимодействия с API ВКонтакте.
    """

    api_url = "https://api.vk.com/method/"

    def __init__(self) -> None:
        self.token = os.getenv("VK_TOKEN")
        self.api_version = "5.199"
        self.logger = setup_logger(
            module_name=get_module_part(__name__), logger_name=__name__
        )
        self.timeout = 10

        self.error_messages = {
            1: "Произошла неизвестная ошибка.",
            3: (
                "Передан неизвестный метод. Проверьте, правильно ли указано "
                "название вызываемого метода: https://vk.com/dev/methods"
            ),
            5: "Авторизация пользователя не удалась.",
            6: "Слишком много запросов в секунду.",
            7: "Нет прав для выполнения этого действия.",
            18: "Страница удалена или заблокирована.",
            29: "Достигнут количественный лимит на вызов метода.",
            30: (
                "Профиль является приватным. Информация, "
                "запрашиваемая о профиле, недоступна с используемым "
                "ключом доступа."
            ),
            100: "Один из необходимых параметров был не передан или неверен.",
            113: "Неверный идентификатор пользователя.",
            200: (
                "Доступ к альбому запрещён. Убедитесь, что Вы "
                "используете верные идентификаторы (для пользователей "
                "owner_id положительный, для сообществ "
                "— отрицательный), и доступ к запрашиваемому контенту "
                "для текущего пользователя есть в полной версии сайта."
            ),
            203: "Доступ к группе запрещён."
        }

        if not self.token:
            raise VKAPIAuthError(
                "VK API token не найден в переменных окружениях"
            )

    def search_users(self) -> list[dict]:
        """Поиск пользователей по заданным параметрам."""

        params = {
            "count": 100,
            "sort": 0,
            "age_from": 18,
            "age_to": 99,
            "status": 6,
        }

        response = self._make_request("users.search", params)
        return response.get("response", {}).get("items", [])

    def get_user_info(self, user_id: int) -> dict:
        """Получение информации о пользователе по его ID."""

        params = {"user_ids": user_id, "fields": "city,sex"}

        response = self._make_request("users.get", params)
        return response.get("response", [])[0]

    def get_user_photos(
        self, user_id: int, album: str = "profile", rev: int = 0
        ) -> dict:
        """Получение информации о фотографиях пользователя."""

        params = {"owner_id": user_id, "album_id": album, "rev": rev}

        response = self._make_request("photos.get", params)
        return response.get("response", {})

    def get_city_info(self, query: str) -> dict:
        """Получение информации о городе по его названию через API ВКонтакте."""

        params = {
            "country_id": 1,
            "q": query,
            "count": 1,
            "need_all": 0
        }

        response = self._make_request("database.getCities", params)
        items = response.get("response", {}).get("items", [])

        if items:
            city = items[0]
            return {"id": city["id"], "title": city["title"]}

        return {}

    def get_group_info(self, city_id: int, query: str) -> list[dict]:
        """Поиск групп по заданному запросу."""

        params = {
            "q": query,
            "city_id": city_id,
            "sort": 6,
            "count": 1,
        }

        response = self._make_request("groups.search", params)
        return response.get("response", {}).get("items", [])

    def get_group_members(self, group_id: int, offset: int = 0) -> list[dict]:
        """Получение списка участников группы."""

        params = {
            "group_id": group_id,
            "count": 1000,
            "offset": offset,
            "fields": "city,sex,last_seen,bdate,relation,\
                can_write_private_message",
        }

        response = self._make_request("groups.getMembers", params)
        return response.get("response", {}).get("items", [])

    def _make_request(self, method: str, params: dict[str, any]) \
        -> dict[str, any]:
        """
        Базовый метод для выполнения запросов к VK API с обработкой ошибок.
        """

        url = self.api_url + method
        params["access_token"] = self.token
        params["v"] = self.api_version

        try:
            response = requests.get(
                url,
                params=params,
                headers={"User-Agent": "VKMatchSensei"},
                timeout=self.timeout,
            )
            data = response.json()
            return self._handle_response_errors(data)
        except (
            requests.exceptions.RequestException,
            ValueError,
            VKAPIError,
            VKAPIAuthError
        ) as e:
            self.logger.error("Ошибка при выполнении запроса: %s", e)
            return {}

    def _handle_response_errors(self, data: dict) -> dict:
        """Обрабатывает ошибки, полученные от VK API."""

        if "error" in data:
            error: dict = data["error"]
            error_code: int = error.get("error_code", 1)
            error_msg: str = error.get("error_msg", "Unknown error")

            error_msg = self.error_messages.get(error_code, error_msg)

            if error_code == 5:
                raise VKAPIAuthError(
                    f"Ошибка авторизации ({error_code}): {error_msg}"
                )

            raise VKAPIError(f"Ошибка от API VK ({error_code}): {error_msg}")

        return data
