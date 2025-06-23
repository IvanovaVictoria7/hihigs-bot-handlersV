# Файл __init__.py.py позволяет обращаться к папке как к модулю
# и импортировать из него содержимое

from .handlers import router
from .bot_commands import set_my_commands
from .logging import setup_logger
from .keyboard import get_main_keyboard

from .handlers import router as main_router
from .bot_commands.load import router as load_router

router = Router()
router.include_router(main_router)
router.include_router(load_router)