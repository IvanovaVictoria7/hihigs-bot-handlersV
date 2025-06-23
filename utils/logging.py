import logging
import os
import sys


def setup_logger(level: int = logging.INFO, fname: str ="bot ") -> None:
    logging.basicConfig(
        format="%(asctime)s %(levelname)s | %(name)s: %(message)s",
        datefmt="[%d-%m-%Y %H:%M:%S]",
        level=level,
        handlers=[logging.FileHandler(f"logs/{fname}.log", mode='a', encoding="utf-8"),
            logging.StreamHandler(sys.stdout)  # вывод в консоль
        ],
    )

# Создаём и экспортируем логгер, чтобы удобно импортировать из других файлов
setup_logger()
logger = logging.getLogger("bot")