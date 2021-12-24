import os
import socket
from typing import Optional


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


class RequestLimiterConfig:
    RATELIMITE_LIMIT = 10
    RATELIMIT_PERIOD = 30
