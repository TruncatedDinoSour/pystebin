"""Pystebin utilities"""

import functools
import os
import random
import re
import string
import types
from functools import wraps

from flask import abort, flash, redirect, request


def unique_filename(directory: str, length: int = 8, __tries: int = 0) -> str:
    filename = "".join((random.choice(string.ascii_letters) for _ in range(20)))

    if os.path.exists(os.path.join(directory, filename)):
        return unique_filename(
            directory, length if __tries < 50 else length + 1, __tries + 1
        )
    return filename


def limit_content_length(max_length):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            cl = request.content_length
            if cl is not None and cl > max_length:
                flash(
                    f"Paste size cannot be larger than {max_length}B, Got {cl}B",
                    "error",
                )
                abort(redirect("/messages"))
            return f(*args, **kwargs)

        return wrapper

    return decorator


def to_snake_case(name):
    name = re.sub("(.)([A-Z][a-z]+)", r"\1_\2", name)
    name = re.sub("__([A-Z])", r"_\1", name)
    name = re.sub("([a-z0-9])([A-Z])", r"\1_\2", name)
    return name.lower()
