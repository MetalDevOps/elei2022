import logging
import logging.handlers
import os
import sys
from datetime import date
from logging.handlers import TimedRotatingFileHandler
from pathlib import Path
import colorlog
from dotenv import load_dotenv

load_dotenv()

logging.captureWarnings(True)



class Error(Exception):
    """Base class for other exceptions"""

    pass


class ParseTokenError(Error):
    """Token can`t be parsed"""

    pass


def get_project_root() -> Path:
    return Path(__file__).parent


def fileNameLocation():
    logs_path = "Logs/"
    if not os.path.exists(logs_path):
        os.makedirs(logs_path)
    today = date.today()
    return f"{get_project_root()}/Logs/{today.day}-{today.month}-{today.year}.log"


log_colors_config = {
    "DEBUG": "cyan",
    "INFO": "green",
    "WARNING": "yellow",
    "ERROR": "red",
    "CRITICAL": "red",
}

FORMATTER = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
fmt = logging.Formatter("%(log_color)s%(levelname)s:%(name)s:%(message)s")
LOG_FILE = fileNameLocation()


def color_handler():
    color_handler = colorlog.ColoredFormatter(
        "%(log_color)s[%(asctime)s] [%(filename)s:%(lineno)d] [%(module)s:%(funcName)s] [%(levelname)s]- %(message)s",
        log_colors=log_colors_config,
    )
    return color_handler


def get_console_handler():
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(color_handler())
    return console_handler


def get_file_handler():
    file_handler = TimedRotatingFileHandler(LOG_FILE, encoding="UTF-8", when="midnight")
    file_handler.setFormatter(FORMATTER)
    return file_handler


def get_logger(logger_name):
    logger = logging.getLogger(logger_name)
    DEBUG = True
    if DEBUG:
        logger.setLevel(logging.DEBUG)  # better to have too much log than not enough
    else:
        logger.setLevel(logging.INFO)
    # logger.setLevel(logging.WARNING)
    # logger.setLevel(logging.CRITICAL)
    logger.addHandler(get_console_handler())
    logger.addHandler(get_file_handler())


    logger.propagate = False
    return logger
