"""Обработчик настройки поиска."""

import re

from config.bot_config import COMMANDS_CONFIG, KEYBOARD_CONFIG, MESSAGES_CONFIG
from db.managers.user_manager import DatabaseUserManager
from services.vk_api.msg_service import MessageService
from services.vk_api.vk_api_service import VKApiService

vk_service = VKApiService()
db_user_manager = DatabaseUserManager()


class SearchSettingsHandler:
    """Обработчик настройки поиска."""

    def __init__(self):
        self.__msg_service = MessageService()
        # Хранение состояния настройки для каждого пользователя
        self.__user_states: dict[int, dict] = {}

    def is_in_search_settings(self, user_id: int) -> bool:
        """Проверяет, находится ли пользователь в процессе настройки поиска."""
        return user_id in self.__user_states

    def handle_search_settings(self, request: str, user_id: int) -> None:
        """Обработчик настройки поиска."""

        # Инициализация настройки поиска
        if request in COMMANDS_CONFIG.get("configure_search_settings"):
            self.__start_search_settings(user_id)
            return

        # Получаем текущее состояние настройки пользователя
        user_state = self.__user_states.get(user_id)
        if not user_state:
            return

        # Обработка каждого шага настройки
        current_step = user_state.get("step")
        if current_step == "age":
            self.__handle_age_setting(user_id, request)
        elif current_step == "sex":
            self.__handle_sex_setting(user_id, request)
        elif current_step == "city":
            self.__handle_city_setting(user_id, request)
        elif current_step == "relation":
            self.__handle_relation_setting(user_id, request)

    def __start_search_settings(self, user_id: int) -> None:
        """Начинает процесс настройки поиска."""
        self.__user_states[user_id] = {"step": "age"}
        self.__msg_service.send_message(
            user_id,
            msg=MESSAGES_CONFIG.get(
                "configure_age", MESSAGES_CONFIG.get("error")
            ),
            btns=KEYBOARD_CONFIG.get("configure_age", None),
        )

    def __handle_age_setting(self, user_id: int, request: str) -> None:
        """Обработка настройки возраста."""

        settings_data = {}

        if request == "пропустить":
            settings_data = {"age_min": 18, "age_max": 99}
        else:
            # Проверка формата возраста (например, "18-25")
            age_match = re.match(r'^(\d+)-(\d+)$', request)
            if not age_match:
                self.__msg_service.send_message(
                    user_id,
                    msg=MESSAGES_CONFIG.get(
                        "configure_age_format_error",
                        MESSAGES_CONFIG.get("error")
                    ),
                    btns=KEYBOARD_CONFIG.get("configure_age", None),
                )
                return

            age_min, age_max = map(int, age_match.groups())
            if not 18 <= age_min <= age_max <= 99:
                self.__msg_service.send_message(
                    user_id,
                    msg=MESSAGES_CONFIG.get(
                        "configure_age_out_of_range_error",
                        MESSAGES_CONFIG.get("error")
                    ),
                    btns=KEYBOARD_CONFIG.get("configure_age", None),
                )
                return

            settings_data = {"age_min": age_min, "age_max": age_max}

        # Сохраняем настройки возраста
        db_user_manager.update_user_settings(user_id, settings_data)

        # Переходим к настройке пола
        self.__user_states[user_id]["step"] = "sex"
        self.__msg_service.send_message(
            user_id,
            msg=MESSAGES_CONFIG.get(
                "configure_sex", MESSAGES_CONFIG.get("error")
            ),
            btns=KEYBOARD_CONFIG.get("configure_sex", None),
        )

    def __handle_sex_setting(self, user_id: int, request: str) -> None:
        """Обработка настройки пола."""

        sex_mapping = {"любой": 0, "женский": 1, "мужской": 2}

        sex = sex_mapping.get(request)
        if sex is None:
            self.__msg_service.send_message(
                user_id,
                msg=MESSAGES_CONFIG.get(
                    "configure_sex_error", MESSAGES_CONFIG.get("error")
                ),
                btns=KEYBOARD_CONFIG.get("configure_sex", None),
            )
            return

        # Сохраняем настройку пола
        db_user_manager.update_user_settings(user_id, {"sex": sex})

        # Переходим к настройке города
        self.__user_states[user_id]["step"] = "city"
        self.__msg_service.send_message(
            user_id,
            msg=MESSAGES_CONFIG.get(
                "configure_city", MESSAGES_CONFIG.get("error")
            ),
            btns=None,
        )

    def __handle_city_setting(self, user_id: int, request: str) -> None:
        """Обработка настройки города."""

        # Получаем информацию о городе через VK API
        city_info = vk_service.get_city_info(request)
        if not city_info:
            self.__msg_service.send_message(
                user_id,
                msg=MESSAGES_CONFIG.get(
                    "configure_city_not_found_error",
                    MESSAGES_CONFIG.get("error")
                ),
                btns=None,
            )
            return

        # Сохраняем настройки города
        settings_data = {
            "city_id": city_info.get("id"),
            "city_title": city_info.get("title")
        }
        db_user_manager.update_user_settings(user_id, settings_data)

        # Переходим к настройке семейного положения
        self.__user_states[user_id]["step"] = "relation"
        self.__msg_service.send_message(
            user_id,
            msg=MESSAGES_CONFIG.get(
                "configure_relation", MESSAGES_CONFIG.get("error")
            ),
            btns=KEYBOARD_CONFIG.get("configure_relation", None),
        )

    def __handle_relation_setting(self, user_id: int, request: str) -> None:
        """Обработка настройки семейного положения."""

        if not re.match(r"^[0-8]$", request) or request is None:
            self.__msg_service.send_message(
                user_id,
                msg=MESSAGES_CONFIG.get(
                    "configure_relation_error", MESSAGES_CONFIG.get("error")
                ),
                btns=KEYBOARD_CONFIG.get("configure_relation", None),
            )
            return

        # Сохраняем настройку семейного положения
        db_user_manager.update_user_settings(user_id, {"relation": int(request)})

        # Завершаем настройку
        del self.__user_states[user_id]  # Очищаем состояние пользователя
        self.__msg_service.send_message(
            user_id,
            msg=MESSAGES_CONFIG.get(
                "configure_search_settings_success",
                MESSAGES_CONFIG.get("error")
            ),
            btns=KEYBOARD_CONFIG.get("main_menu", None),
        )
