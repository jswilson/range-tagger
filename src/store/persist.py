from functools import wraps

from ..components.serialize import Serializer

def persist_state(f):
    @wraps(f)
    def wrapped(*args, **kwargs):
        r = f(*args, **kwargs)

        json = Serializer.store_to_json(args[0])
        with open('range-tagger.seg', 'w') as file:
            file.write(json)

        return r
    return wrapped
