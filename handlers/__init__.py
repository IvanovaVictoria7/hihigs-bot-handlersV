# Файл __init__.py.py позволяет обращаться к папке как к модулю
# и импортировать из него содержимое

from .handlers import router
from .bot_commands import set_my_commands
from .logging import setup_logger
from .keyboard import get_main_keyboard

