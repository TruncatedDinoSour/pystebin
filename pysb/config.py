import os
from typing import Optional

WEBSITE_NAME: str = os.path.split(os.path.abspath("."))[1]
PASTE_DIR: str = "pastes"
MAX_PASTE_SIZE_B: int = 1_000_000
HOST: str = "127.0.0.1"
PORT: int = 5050
DEBUG: bool = True
SECRET_KEY: bytes = os.urandom(20_000_000)
MAX_PASTE_COUNT: Optional[int] = 3  # or for example 100, None disables it


class RequestLimiterConfig:
    RATELIMITE_LIMIT = 10
    RATELIMIT_PERIOD = 30
