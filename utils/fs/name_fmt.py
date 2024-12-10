"""Модуль вспомогательных функций для работы с именами модулей."""

from utils.logging.setup import setup_logger


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


def get_module_part(module: str, idx: int = -1, sep: str = ".") -> str:
    """
    Возвращает часть строки, разделенной по разделителю.
    
    ### Аргументы:
    - `module` (str): Строка, которую нужно разделить.
    - `idx` (int): Индекс части строки, которую нужно вернуть. 
      По умолчанию будет получена последняя часть (индекс -1).
    - `sep` (str): Разделитель. По умолчанию `.`
    
    ### Примеры:
    ```python
    >>> get_module_part("utils.fs.formatter", idx=-1)
    >>> # => 'formatter' — сам модуль (последняя часть пути)
    >>> get_module_part("utils.fs.formatter", idx=0)
    >>> # => 'utils' — Пакет (первая часть пути)
    >>> get_module_part("utils.fs.formatter", idx=1)
    >>> # => 'fs' — Подпакет пакета db (вторая часть пути)
    ```
    """

    if not module:
        logger.error(
            "Строка не содержит никаких символов. Возвращена пустая строка."
            )
        return ""

    if sep not in module:
        logger.error(
            "Строка не содержит разделителя. Возвращена строка без изменений."
            )
        return module

    parts: list[str] = module.split(sep)

    if idx < -len(parts) or idx >= len(parts):
        logger.error(
            f"Индекс ({idx}) выходит за пределы доступных частей "
            f"({len(parts)}).\nБыл выбран последний индекс (-1).\n"
            f"Был передан модуль: '{module}'.\nВозвращен: '{parts[-1]}'."
            )
        return parts[-1]

    return parts[idx]


logger = setup_logger(get_module_part(__name__, idx=0), logger_name=__name__)
