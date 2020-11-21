import json
from enum import Enum
from functools import partial


def signed_num_bin_width(num: int):
    """
    Returns least binary width to hold the specified signed `num`.

    >>> signed_num_bin_width(10)
    5
    >>> signed_num_bin_width(-1)
    2
    >>> signed_num_bin_width(-2)
    3
    >>> signed_num_bin_width(0)
    2
    """

    return len("{:+b}".format(num))


def unsigned_num_bin_width(num: int):
    """
    Returns least binary width to hold the specified unsigned `num`.

    >>> unsigned_num_bin_width(10)
    4
    >>> unsigned_num_bin_width(1)
    1
    >>> unsigned_num_bin_width(0)
    1
    >>> unsigned_num_bin_width(-1)
    Traceback (most recent call last):
    ...
    ValueError: Unexpected negative number: -1
    """

    if num < 0:
        raise ValueError(f"Unexpected negative number: {num}")

    return len("{:b}".format(num))


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
