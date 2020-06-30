import json
import pickle
import dill


def cache_return(func, path):
    def wrapped(func):
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            with open(path, "w") as f:
                json.dump(result, f)
            return result
        return wrapper
    return wrapped


from datetime import datetime


def gen_file_name(directive="%Y-%m-%d"):
    return datetime.now().strftime(directive)
