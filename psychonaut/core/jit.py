import os
from functools import wraps

USING_NUMBA = False

try:
    assert 'NUMBA_DISABLE_JIT' not in os.environ
    from numba import jit
    USING_NUMBA = True
except (ImportError, AssertionError):
    def jit(*args, **kwargs):
        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                return func(*args, **kwargs)
            return wrapper
        return decorator
