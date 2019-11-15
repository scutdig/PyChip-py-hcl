from ..shortcuts import uw
from ..type_measurer import equal
from ..expr.mux import Mux


class MuxTypeChecker(object):
    mux_checker_map = {}

    @staticmethod
    def check(op_obj):
        try:
            return MuxTypeChecker.mux_checker_map[type(op_obj)](op_obj)
        except KeyError:
            raise NotImplementedError(type(op_obj))


def checker(mux):
    def f(func):
        MuxTypeChecker.mux_checker_map[mux] = func
        return func

    return f


@checker(Mux)
def _(mux):
    if not equal(mux.cond, uw(1)):
        return False
    if not equal(mux.tval.tpe, mux.fval.tpe):
        return False
    if not equal(mux.tval.tpe, mux.tpe):
        return False
    return True
