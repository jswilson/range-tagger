from functools import wraps
import os

from ..components.serialize import Serializer
from ..registry import Registry

def persist_state(f):
    @wraps(f)
    def wrapped(*args, **kwargs):
        r = f(*args, **kwargs)

        json = Serializer.store_to_json(args[0])

        try:
            with open(Registry.CONFIG_FILE_LOCATION, 'w') as file:
                file.write(json)
        except FileNotFoundError:
            os.makedirs(os.path.dirname(Registry.CONFIG_FILE_LOCATION))
            with open(Registry.CONFIG_FILE_LOCATION, 'w') as file:
                file.write(json)

        return r
    return wrapped
