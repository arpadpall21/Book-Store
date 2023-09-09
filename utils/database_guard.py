import functools


def check_connection(fn):
    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        database = args[0]
        database._check_connection()
        return fn(*args, **kwargs)
    return wrapper
