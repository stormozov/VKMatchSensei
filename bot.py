"""
Основной модуль бота VKMatchSensei.

Этот модуль содержит реализацию бота VKMatchSensei, который взаимодействует с 
API ВКонтакте для отправки сообщений пользователям и обработки событий 
в чате группы.

### Классы:
- `VKMatchSenseiBot`: Основной класс бота, который управляет всеми функциями.

### Пример использования:
```python
if __name__ == "__main__":
    bot = VKMatchSenseiBot(<VK_GROUP_TOKEN>)
    bot.run()
```
"""

import os
import json
from vk_api.longpoll import VkEventType, VkLongPoll
from dotenv import load_dotenv

from handlers.command_handler import CommandHandler
from services.vk_api.auth_vk_service import AuthVKService

load_dotenv()


class VKMatchSenseiBot:
    """Бот VKMatchSensei."""

    __cmd_handler = CommandHandler()

    def __init__(self, group_token: str = os.getenv("VK_GROUP_TOKEN")) -> None:
        self.token = group_token
        self.vk = AuthVKService().auth_vk_group(self.token)
        self.longpoll = VkLongPoll(self.vk)
        self.user_id = None

    def run(self) -> None:
        """Запускает бот."""
        for event in self.longpoll.listen():
            if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                # Получаем текст сообщения
                request = event.text.strip().lower()
                self.user_id = event.user_id

                # Проверяем наличие payload в сообщении
                try:
                    payload = json.loads(event.payload)
                    # Если есть payload, обрабатываем его
                    self.handle_payload(payload, request)
                except (json.JSONDecodeError, AttributeError):
                    # Если payload нет или он некорректен, обрабатываем текст
                    self.handle_message(request)

    def handle_payload(self, payload: dict, request: str) -> None:
        """Обработка сообщений с payload от кнопок."""
        # Передаем в обработчик настроек поиска и текст, и payload
        self.__cmd_handler.search_settings_handler(request, self.user_id)

    def handle_message(self, request: str) -> None:
        """Обработка текстовых сообщений."""
        if request in ("/start", "/начать", "начать"):
            self.__cmd_handler.start_handler(self.user_id)
        elif request in ("настроить поиск",):
            self.__cmd_handler.search_settings_handler(request, self.user_id)
        else:
            # Все остальные сообщения передаем в обработчик настроек
            # для обработки текстового ввода (например, возраст или город)
            self.__cmd_handler.search_settings_handler(request, self.user_id)


def main() -> None:
    """Запуск бота."""
    bot = VKMatchSenseiBot()
    print("Бот запущен!")
    bot.run()


if __name__ == "__main__":
    main()
