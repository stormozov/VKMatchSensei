"""Сервис для работы с сообщениями бота."""

import os
from vk_api.keyboard import MAX_BUTTONS_ON_LINE, VkKeyboard, VkKeyboardColor

from services.vk_api.auth_vk_service import AuthVKService


class MessageService:
    """Класс для работы с сообщениями бота."""

    def __init__(self, group_token: str = os.getenv("VK_GROUP_TOKEN")) -> None:
        self.vk = AuthVKService().auth_vk_group(group_token)

    def send_message(
        self,
        user_id: int,
        msg: str,
        btns: dict = None,
        attachment: str = None
        ) -> None:
        """
        Отправка сообщения пользователю в чате.
        
        ### Аргументы:
        - user_id (int): Идентификатор пользователя, которому будет 
          отправлено сообщение.
        - msg (str): Текст сообщения.
        - btns (str, optional): Словарь с настройками клавиатуры, которые будут 
          преобразованы в JSON для последующей отправки боту. По умолчанию None.
        - attachment (str, optional): Прикрепленная картинка. Нужно указать 
          в виде строки. По умолчанию None.
        
        ### Примеры:
        ```python
        >>> send_message(123456, "Привет!")
        >>> send_message(123456, "Привет!", attachment="photo123456_123456")
        ```
        """

        if btns is not None:
            btns = self._create_markup(btns)

        self.vk.method(
            "messages.send",
            {
                "user_id": user_id,
                "message": msg,
                "keyboard": btns,
                "attachment": attachment,
                "random_id": 0
            }
        )

    def _create_markup(
        self, btns: dict[str, str | bool | list[dict[str, str]]]
        ) -> str:
        """Метод для создания клавиатуры.

        ### Аргументы:
        - btns (dict): Словарь с настройками клавиатуры. Например: \
            `{"one_time": True, "inline": False, "actions": []}`

        ### Возвращает:
        - str: Отформатированный формат данных для передачи боту для создания 
          клавиатуры.
        """
        keyboard = self._create_layout(btns)
        return keyboard.get_keyboard()

    def _create_layout(self, btns: dict[str, str | bool | list]) \
        -> VkKeyboard | None:
        """Метод для создания разметки клавиатуры."""

        keyboard = VkKeyboard(
            one_time=btns.get("one_time", True),
            inline=btns.get("inline", False)
        )

        actions = btns.get("actions", [])
        if actions and isinstance(actions[0], list):
            self._add_buttons_by_rows(keyboard, actions)
        else:
            self._add_buttons_in_line(keyboard, actions)

        return keyboard

    def _add_buttons_by_rows(self, keyboard: VkKeyboard, rows: list[list[dict]]) \
        -> None:
        """Метод для добавления кнопки в клавиатуру по строкам."""
        for row_index, row in enumerate(rows):
            if row_index > 0:
                keyboard.add_line()
            self._add_buttons_in_line(keyboard, row)

    def _add_buttons_in_line(self, keyboard: VkKeyboard, buttons: list[dict]) \
        -> None:
        """
        Метод для добавления кнопки в одну строку клавиатуры.
        
        ### Исключения:
        - ValueError: Если количество кнопок в строке превышает максимальное.
        """

        if len(buttons) > MAX_BUTTONS_ON_LINE:
            raise ValueError(
                f"Макс. кол-во кнопок в одной строке - {MAX_BUTTONS_ON_LINE}"
            )

        for btn in buttons:
            keyboard.add_button(
                label=btn.get("label"),
                color=btn.get("color", VkKeyboardColor.SECONDARY),
                payload=btn.get("payload", None)
            )
