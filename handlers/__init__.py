from .handlers import router as router
from .callbacks import router as callbacks_router
from .bot_commands import set_my_commands
from .logging import setup_logger
from .keyboard import get_main_keyboard

__all__ = [
    "router",
    "set_my_commands",
    "setup_logger",
    "get_main_keyboard",
    "callbacks_router"
]


