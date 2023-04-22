import asyncio
from functools import wraps
import sys


def as_async(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        return asyncio.run(func(*args, **kwargs))

    return wrapper



def print_error_and_fail(msg: str):
    print(msg, file=sys.stderr)
    sys.exit(1)


def clean_handle(handle: str) -> str:
    if handle.startswith("@"):
        handle = handle[1:]
    return handle