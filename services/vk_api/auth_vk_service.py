"""Сервис для работы с аутентификацией через ВКонтакте."""

import vk_api

from services.formatters.module_formatters import get_module_part
from utils.logging.setup import setup_logger


class AuthVKService:
    """Сервис для работы с аутентификацией через ВКонтакте."""

    def __init__(self) -> None:
        self.logger = setup_logger(
            module_name=get_module_part(__name__, idx=0),
            logger_name="main_script"
            )

    def auth_vk_group(self, token: str) -> vk_api.VkApi:
        """Аутентификация в VK API."""
        try:
            return vk_api.VkApi(token=token)
        except vk_api.AuthError as error_msg:
            self.logger.error(error_msg)
            raise error_msg
