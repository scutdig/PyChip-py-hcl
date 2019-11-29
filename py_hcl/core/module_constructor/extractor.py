from . import module_err
from ...dsl.expression import Expression


def extract(dct):
    res = {}

    for k in dct:
        if isinstance(dct[k], Expression):
            res[k] = dct[k]

    if 'io' not in res:
        raise module_err('NotContainsIO')

    return res
