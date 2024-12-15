"""Модуль для создания клавиатуры."""

from vk_api.keyboard import VkKeyboard


class VKKeyboardManager:
    """Менеджер для создания клавиатур в боте."""

    def create_markup(
        self, btns: dict[str, str | bool | list[dict[str, str]]]
        ) -> str | None:
        """Метод для создания клавиатуры.

        ### Аргументы:
        - btns (dict): Словарь с настройками клавиатуры. Например: \
            `{"one_time": True, "inline": False, "actions": []}`

        ### Возвращает:
        - str: Отформатированный формат данных для передачи боту для создания \
            клавиатуры.
        """

        keyboard = self._create_layout(btns)
        return keyboard.get_keyboard()

    def _create_layout(self, btns: dict[str, str | bool | list]) \
        -> VkKeyboard | None:
        """Метод для создания разметки клавиатуры."""

        keyboard = VkKeyboard(btns.get("one_time"), btns.get("inline"))

        for btn in btns.get("actions"):
            keyboard.add_button(
                label=btn.get("label"),
                color=btn.get("color", "secondary"),
                payload=btn.get("payload", None)
                )

        return keyboard
