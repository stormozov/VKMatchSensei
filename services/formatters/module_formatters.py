"""Сервис форматирования именен модулей."""

from utils.logging.setup import setup_logger


def replace_sep_in_module_name(
    module: str, old_sep: str = ".", new_sep: str = "_"
    ) -> str:
    """
    Возвращает имя модуля в формате, который можно использовать в имени файла 
    или директории.
    
    ### Например:
    ```python
    >>> replace_sep_in_module_name("utils.fs.formatter")
    >>> # => 'utils_fs_formatter'
    ```
    """

    validation_result = validate_replace_sep_in_module_name(
        module, old_sep, new_sep
        )

    if validation_result is not None:
        return validation_result

    return module.replace(old_sep, new_sep)


def get_module_part(module: str, idx: int = -1, sep: str = ".") -> str:
    """
    Возвращает часть строки, разделенной по разделителю.
    
    ### Аргументы:
    - module (str): Строка, которую нужно разделить.
    - idx (int): Индекс части строки, которую нужно вернуть. 
      По умолчанию будет получена последняя часть (индекс -1).
    - sep (str): Разделитель. По умолчанию `.`
    
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

    validation_result = validate_module_part(module, idx, sep)

    if validation_result is not None:
        return validation_result

    return module.split(sep)[idx]


def validate_replace_sep_in_module_name(
    module: str, old_sep: str, new_sep: str
    ) -> str | None:
    """Проверяет корректность пути."""

    if not isinstance(module, str) or not isinstance(old_sep, str) \
        or not isinstance(new_sep, str):
        logger.error("Все параметры должны быть строками.")
        return "default"

    if not module:
        logger.error("Строка модуля не должна быть пустой.")
        return "default"

    if old_sep not in module:
        logger.error("Разделитель '%s' не найден в строке модуля.", old_sep)
        return module

    return None


def validate_module_part(module: str, idx: int, sep: str) -> str | None:
    """Проверяет корректность строки и индекса."""

    if not module:
        logger.error(
            "Строка не содержит никаких символов. Возвращена строка 'default'."
            )
        return "default"

    if sep not in module:
        logger.error(
            "Строка '%s' не содержит разделителя. Возвращена строка без \
            изменений.", module
            )
        return module

    parts: list[str] = module.split(sep)

    if idx < -len(parts) or idx >= len(parts):
        logger.error(
            "Индекс (%s) выходит за пределы доступных частей (%s).\n\
            Был выбран последний индекс (-1).\n\
            Был передан модуль: '%s'.\nВозвращен: '%s'.",
            idx, len(parts), module, parts[-1]
            )
        return parts[-1]

    return None


logger = setup_logger(get_module_part(__name__, idx=1), logger_name=__name__)
