"""Пакет сервисов работы с API ВКонтакте."""

from .vk_api_service import VKApiService
from .msg_service import MessageService
from .auth_vk_service import AuthVKService

__all__ = [
    "VKApiService",
    "MessageService",
    "AuthVKService",
]
