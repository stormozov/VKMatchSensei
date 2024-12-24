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
                request = event.text.strip().lower()
                self.user_id = event.user_id
                self.handle_message(request)

    def handle_message(self, request: str) -> None:
        """Обработка текстовых сообщений."""

        if request in ("/start", "/начать", "начать"):
            self.__cmd_handler.start_handler(self.user_id)
        elif request == "настроить поиск":
            self.__cmd_handler.search_settings_handler(request, self.user_id)
        elif self.__cmd_handler.is_in_search_settings(self.user_id):
            # Передаем сообщение в обработчик настроек только если пользователь
            # находится в процессе настройки
            self.__cmd_handler.search_settings_handler(request, self.user_id)
        elif request == "начать поиск":
            self.__cmd_handler.start_searching(self.user_id)
        else:
            # Обработка неизвестных команд
            self.__cmd_handler.handle_unknown_message(self.user_id)


def main() -> None:
    """Запуск бота."""
    bot = VKMatchSenseiBot()
    print("Бот запущен!")
    bot.run()


if __name__ == "__main__":
    main()
