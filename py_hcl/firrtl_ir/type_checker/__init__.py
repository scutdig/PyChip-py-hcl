from .mux_checker import MuxTypeChecker
from .op_checker import OpTypeChecker


def check(obj):
    try:
        return OpTypeChecker.check(obj)
    except NotImplementedError:
        pass

    try:
        return MuxTypeChecker.check(obj)
    except NotImplementedError:
        pass

    return False
