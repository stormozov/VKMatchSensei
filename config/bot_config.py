"""
Модуль для централизованного хранения конфигураций бота в формате Python словаря.

### Доступные конфигурации:
- COMMANDS_CONFIG: конфигурация команд бота.
- KEYBOARD_CONFIG: конфигурация клавиатуры бота.
- MESSAGES_CONFIG: конфигурация сообщений бота.
"""

from utils.fs.json_manager import JSONManager


JSON_MANAGER = JSONManager()

COMMANDS_CONFIG = JSON_MANAGER.get_bot_settings_from_json(config_name="commands")
KEYBOARD_CONFIG = JSON_MANAGER.get_bot_settings_from_json(config_name="keyboard")
MESSAGES_CONFIG = JSON_MANAGER.get_bot_settings_from_json(config_name="messages")
