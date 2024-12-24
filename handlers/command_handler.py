"""Модуль для обработки команд бота."""

from handlers.basic_handlers import BasicHandler
from handlers.search_handler import SearchHandler


class CommandHandler(BasicHandler, SearchHandler):
    pass
