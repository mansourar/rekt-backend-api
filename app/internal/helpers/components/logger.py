import logging
import os
import sys
from datetime import datetime


def init(main_dir: str):
    log_format = "%(levelname)s | %(asctime)s | %(name)s | %(message)s"
    formatter = logging.Formatter(log_format)
    log_level = os.getenv("LOG_LEVEL", "DEBUG")
    handlers = []

    log_to_file = int(os.getenv("FILE_LOGGER", "0"))
    if bool(log_to_file):
        parent_dir = os.path.abspath(os.path.join(main_dir, os.pardir))
        logs_dir = os.path.join(parent_dir, "logs")
        os.makedirs(logs_dir, exist_ok=True)
        now = datetime.now()
        timestamp = now.strftime("%Y%m%d_%H%M%S")
        file_handler = logging.FileHandler(os.path.join(logs_dir, f"{timestamp}.log"))
        file_handler.setLevel(log_level)
        file_handler.setFormatter(formatter)
        handlers.append(file_handler)

    log_to_console = int(os.getenv("CONSOLE_LOGGER", "0"))
    if bool(log_to_console):
        console_handler = logging.StreamHandler()
        console_handler.setLevel(log_level)
        console_handler.setFormatter(formatter)
        handlers.append(console_handler)

    logger = logging.getLogger(__name__)
    log_unhandled_exception(logger)
    logging.basicConfig(format=log_format, level=log_level, handlers=handlers, force=True)


def log_unhandled_exception(logger):
    def excepthook(exc_type, exc_value, traceback):
        if issubclass(exc_type, KeyboardInterrupt):
            # If the exception is a KeyboardInterrupt, don't log it
            sys.__excepthook__(exc_type, exc_value, traceback)
            return

        logger.exception("Unhandled exception", exc_info=(exc_type, exc_value, traceback))

    sys.excepthook = excepthook
