import logging
import os
import socket
from typing import Optional

from werkzeug import exceptions as http_exceptions

from .util import to_snake_case


def get_ip() -> str:
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("10.255.255.255", 1))  # Does not have to be reachable
        IP = s.getsockname()[0]
    except Exception:
        IP = "127.0.0.1"
    finally:
        s.close()
    return IP


WEBSITE_NAME: str = os.path.split(os.path.abspath("."))[1]
PASTE_DIR: str = "pastes"
MAX_PASTE_SIZE_B: int = 1_000_000
HOST: str = get_ip()
PORT: int = 5050
DEBUG: bool = True
SECRET_KEY: bytes = os.urandom(20_000_000)
MAX_PASTE_COUNT: Optional[int] = None  # or for example 100, None disables it
REQUEST_CODES: dict[int, str] = {}

for exception in dir(http_exceptions):
    if exception.startswith("__"):
        continue
    try:
        REQUEST_CODES[getattr(http_exceptions, exception).code] = to_snake_case(
            exception
        )
    except AttributeError:
        pass

LOG_DIR: str = "logs"
LOGGING_CONFIG: dict = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "debug.log": {
            "class": "logging.handlers.TimedRotatingFileHandler",
            "backupCount": 5,
            "level": logging.DEBUG,
            "filename": os.path.join(LOG_DIR, "debug.log"),
        },
        "error.log": {
            "class": "logging.handlers.TimedRotatingFileHandler",
            "backupCount": 5,
            "level": logging.ERROR,
            "filename": os.path.join(LOG_DIR, "error.log"),
        },
    },
    "loggers": {
        "": {"handlers": ["error.log"], "level": logging.ERROR},
        "debug_log": {"handlers": ["debug.log"], "level": logging.DEBUG},
    },
}


class RequestLimiterConfig:
    RATELIMITE_LIMIT = 10
    RATELIMIT_PERIOD = 30
