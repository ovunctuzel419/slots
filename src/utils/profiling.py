import time
from functools import wraps


def timedfunc(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = fn(*args, **kwargs)
        end = time.perf_counter()
        elapsed_ms = (end - start) * 1000
        print(f"{fn.__name__} took {elapsed_ms:.5f} ms")
        return result
    return wrapper
