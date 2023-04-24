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


HANDLE_WARNING = """WARNING:

You input handle,
    {}
which looks like an email address but should probably look like,
    @{}
"""

def clean_handle(handle: str) -> str:
    if handle.startswith("@"):
        handle = handle[1:]

    idx = handle.find("@")
    if idx != -1 and (0 < idx < len(handle) - 1):
        suggestion = handle.replace("@", ".")
        print(HANDLE_WARNING.format(handle, suggestion), file=sys.stderr)
    

    return handle