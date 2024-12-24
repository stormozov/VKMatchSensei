"""Сервис для работы с API ВКонтакте"""

import os
import requests
from dotenv import load_dotenv

load_dotenv()


class VKApiService:
    """
    Сервис для работы с API ВКонтакте.
    
    Содержит различные методы для взаимодействия с API ВКонтакте.
    """

    api_url = "https://api.vk.com/method/"

    def __init__(self) -> None:
        self.token = os.getenv("VK_TOKEN")
        self.api_version = "5.199"

    def search_users(self):
        """Поиск пользователей по заданным параметрам."""

        url = self.api_url + "users.search"
        params = {
            "access_token": self.token,
            "v": self.api_version,
            "count": 100,
            "sort": 0,
            "age_from": 18,
            "age_to": 99,
            "status": 6,
        }

        response = requests.get(url, params=params, timeout=10)

        return response.json().get("response", {}).get("items", [])

    def get_user_info(self, user_id) -> dict:
        """Получение информации о пользователе по его ID."""

        url = self.api_url + "users.get"
        params = {
            "user_ids": user_id,
            "access_token": self.token,
            "v": self.api_version,
            "fields": "city, sex",
        }

        response = requests.get(url, params=params, timeout=10)

        return response.json().get("response", [])[0]

    def get_city_info(self, query: str) -> dict | None:
        """
        Получение информации о городе по его названию через API ВКонтакте.
        
        ### Аргументы:
        - query (str): Название города для поиска.
        
        ### Возвращает:
        - dict: Словарь с информацией о городе или None, \
          если город не найден. Формат возвращаемого словаря: \
          {'id': int, 'title': str}
        - None: Если город не найден, либо возникло исключение \
          "RequestException", "KeyError", "IndexError"
        """

        url = self.api_url + "database.getCities"
        params = {
            "access_token": self.token,
            "v": self.api_version,
            "country_id": 1,
            "q": query,
            "count": 1,
            "need_all": 0
        }

        try:
            data = requests.get(url, params=params, timeout=10).json()

            if "response" in data and "items" in data["response"] \
                and data["response"]["items"]:
                city = data["response"]["items"][0]
                return {"id": city["id"], "title": city["title"]}
            return None
        except (requests.RequestException, KeyError, IndexError):
            return None

    def get_group_info(self, city_id: int, query: str) -> list:
        """Поиск групп по заданному запросу."""

        url = self.api_url + "groups.search"
        params = {
            "access_token": self.token,
            "v": self.api_version,
            "q": query,
            "city_id": city_id,
            "sort": 6,
            "count": 1,
        }

        response = requests.get(url, params=params, timeout=10)
        response = response.json().get("response", {}).get("items", [])

        return response

    def get_group_members(self, group_id: int, offset: int = 0) -> list[dict]:
        """Получение списка участников группы."""

        url = self.api_url + "groups.getMembers"
        params = {
            "access_token": self.token,
            "v": self.api_version,
            "group_id": group_id,
            "count": 1000,
            "offset": offset,
            "fields": "city,sex,last_seen,bdate,relation,can_write_private_message",
        }

        response = requests.get(url, params=params, timeout=10)
        return response.json().get("response", {}).get("items", [])
