from .mux import MuxTypeChecker
from .op import OpTypeChecker
from .accessor import AccessorTypeChecker


def check(obj):
    try:
        return OpTypeChecker.check(obj)
    except NotImplementedError:
        pass

    try:
        return MuxTypeChecker.check(obj)
    except NotImplementedError:
        pass

    try:
        return AccessorTypeChecker.check(obj)
    except NotImplementedError:
        pass

    return False
