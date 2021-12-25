#!/usr/bin/env python3
"""Pystebin example app"""

import sys

from pysb import create_app
from pysb.config import DEBUG, HOST, PORT


def main() -> int:
    """Entry/main function"""

    create_app().run(HOST, PORT, DEBUG)

    return 0


if __name__ == "__main__":
    assert main.__annotations__.get("return") is int, "main() should return an integer"
    sys.exit(main())
