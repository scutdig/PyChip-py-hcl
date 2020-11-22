import json
from enum import Enum
from functools import partial


def json_serialize(cls=None, json_fields=()):
    def rec(v):
        if hasattr(v, "json_obj"):
            return v.json_obj()
        elif isinstance(v, dict):
            return {k: rec(v) for k, v in v.items()}
        elif isinstance(v, (list, tuple)):
            return [rec(v) for v in v]
        elif isinstance(v, Enum):
            return v.name
        return v

    def serialize(self):
        return json.dumps(self.json_obj(), indent=2)

    def _(_cls, _json_fields):
        def js(self):
            if len(_json_fields) == 0:
                kv = vars(self)
            else:
                kv = {f: vars(self)[f] for f in _json_fields}

            return {k: rec(v) for k, v in kv.items()}

        _cls.json_obj = js
        _cls.__str__ = serialize
        return _cls

    if cls:
        return _(cls, json_fields)

    return partial(_, _json_fields=json_fields)
