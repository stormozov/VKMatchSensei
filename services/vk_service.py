"""Сервис для работы с API ВКонтакте"""

import os
import requests
from dotenv import load_dotenv

load_dotenv()


class VKService:
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
            'access_token': self.token,
            'v': self.api_version,
            'count': 100,
            'sort': 0,
            'age_from': 18,
            'age_to': 99,
            'status': 6,
        }

        response = requests.get(url, params=params)

        return response.json().get('response', {}).get('items', [])

    def get_user_info(self, user_id):
        """Получение информации о пользователе."""

        url = self.api_url + "users.get"
        params = {
            'user_ids': user_id,
            'access_token': self.token,
            'v': self.api_version,
        }

        response = requests.get(url, params=params)

        return response.json().get('response', [])[0]
