"""
Основной модуль бота VKMatchSensei.

Этот модуль содержит реализацию бота VKMatchSensei, который взаимодействует с 
API ВКонтакте для отправки сообщений пользователям и обработки событий 
в чате группы.

### Импортируемые библиотеки:
- `os`: Для работы с операционной системой и переменными окружения.
- `vk_api`: Библиотека для работы с API ВКонтакте.
- `vk_api.longpoll`: Модуль для работы с API ВКонтакте через LongPoll.
- `dotenv`: Для работы с переменными окружения.

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
import vk_api
from vk_api.longpoll import VkEventType, VkLongPoll
from dotenv import load_dotenv

from utils.fs.name_fmt import get_module_part
from utils.logging.setup import setup_logger

load_dotenv()

logger = setup_logger(get_module_part(__name__, idx=0), logger_name=__name__)


class VKMatchSenseiBot:
    """Бот VKMatchSensei."""

    def __init__(self, group_token: str) -> None:

        self.token = group_token
        self.vk = self.authenticate_vk(self.token)
        self.longpoll = VkLongPoll(self.vk)

        self.user_id = None

    def authenticate_vk(self, token: str) -> vk_api.VkApi:
        """Аутентификация в VK API."""

        try:
            return vk_api.VkApi(token=token)
        except vk_api.AuthError as error_msg:
            logger.error(error_msg)
            raise error_msg

    def send_message(
        self,
        user_id: int,
        msg: str,
        attachment: str = None,
        ) -> None:
        """
        Отправка сообщения пользователю в чате.
        
        ### Аргументы:
        - `user_id` (int): Идентификатор пользователя.
        - `msg` (str): Текст сообщения.
        - `attachment` (str, optional): Приложение.
        
        ### Примеры:
        ```python
        >>> send_message(123456, "Привет!")
        >>> send_message(123456, "Привет!", attachment="photo123456_123456")
        ```
        """

        self.vk.method(
            "messages.send",
            {
                "user_id": user_id,
                "message": msg,
                "attachment": attachment,
                "random_id": 0
            }
        )

    def run(self) -> None:
        """Запускает бот."""

        for event in self.longpoll.listen():
            if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                self.user_id = event.user_id
                self.send_message(self.user_id, "Привет!")


def main() -> None:
    bot = VKMatchSenseiBot(os.getenv("VK_GROUP_TOKEN"))
    bot.run()


if __name__ == "__main__":
    main()
