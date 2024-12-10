"""Модуль вспомогательных функций для работы с именами модулей."""

from utils.logging.config import setup_logger


def format_module_name(module: str, sep: str = "_") -> str:
    """
    Возвращает имя модуля в формате, который можно использовать в имени файла 
    или директории.
    
    ### Например:
    ```python
    >>> format_module_name("utils.fs.formatter")
    >>> # => 'utils_fs_formatter'
    ```
    """
    return module.replace(".", sep)


def get_module_part(module: str, index: int = -1, sep: str = ".") -> str:
    """
    Возвращает часть строки, разделенной по разделителю.
    
    ### Аргументы:
    - `module` (str): Строка, которую нужно разделить.
    - `index` (int): Индекс части строки, которую нужно вернуть. 
      По умолчанию будет получена последняя часть (индекс -1).
    - `sep` (str): Разделитель. По умолчанию `.`
    
    ### Примеры:
    ```python
    >>> get_module_part("utils.fs.formatter", index=-1)
    >>> # => 'formatter' — сам модуль (последняя часть пути)
    >>> get_module_part("utils.fs.formatter", index=0)
    >>> # => 'utils' — Пакет (первая часть пути)
    >>> get_module_part("utils.fs.formatter", index=1)
    >>> # => 'fs' — Подпакет внутри пакета db (вторая часть пути)
    ```
    """

    if not module:
        logger.error(
            "Строка не содержит никаких символов. Возвращена пустая строка."
            )
        return ""

    if sep not in module:
        logger.error(
            "Строка не содержит разделителя. Возвращена пустая строка."
            )
        return ""

    parts: list[str] = module.split(sep)

    if index < -len(parts) or index >= len(parts):
        logger.error(f"Индекс ({index}) выходит за пределы доступных частей "
                     f"({len(parts)}).\n" 
                     "Был выбран последний индекс (-1).\n"
                     f"Был передан модуль: '{module}'.\n" 
                     f"Возвращен: '{parts[-1]}'."
                     )
        return parts[-1]

    return parts[index]


logger = setup_logger(get_module_part(__name__, index=0), logger_name=__name__)
