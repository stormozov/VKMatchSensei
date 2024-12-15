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
import vk_api
from vk_api.longpoll import VkEventType, VkLongPoll
from dotenv import load_dotenv

from handlers.command_handler import CommandHandler
from utils.fs.name_fmt import get_module_part
from utils.keyboard.keyboard import VKKeyboardManager
from utils.logging.setup import setup_logger

load_dotenv()

logger = setup_logger(get_module_part("main", idx=0), logger_name="main_script")


class VKMatchSenseiBot:
    """Бот VKMatchSensei."""

    __cmd_handler = CommandHandler()
    __keyboard = VKKeyboardManager()

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

    def run(self) -> None:
        """Запускает бот."""

        for event in self.longpoll.listen():
            if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                request = event.text.strip().lower()
                self.user_id = event.user_id
                self.handlers(request)

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
        - user_id (int): Идентификатор пользователя, которому будет \
            отправлено сообщение.
        - msg (str): Текст сообщения.
        - btns (str): Словарь с настройками клавиатуры, которые будут \
            преобразованы в JSON для последующей отправки боту. \
            По умолчанию None.
        - attachment (str, optional): Прикрепленная картинка. Нужно указать \
            в виде строки. По умолчанию None.
        
        ### Примеры:
        ```python
        >>> send_message(123456, "Привет!")
        >>> send_message(123456, "Привет!", attachment="photo123456_123456")
        ```
        """

        if btns is not None:
            btns = self.__keyboard.create_markup(btns)

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

    def handlers(self, request: str) -> None:
        """Обработчики событий."""

        if request in ("/start", "/начать", "начать"):
            self.__cmd_handler.start_handler(self.user_id, self.send_message)


def main() -> None:
    """Запуск бота."""
    bot = VKMatchSenseiBot(os.getenv("VK_GROUP_TOKEN"))
    print("Бот запущен!")
    bot.run()


if __name__ == "__main__":
    main()
