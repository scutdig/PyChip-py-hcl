from py_hcl.core.expr import HclExpr
from py_hcl.core.expr.error import ExprError
from py_hcl.core.expr.place import ExprPlace
from py_hcl.core.hcl_ops import hcl_operation
from py_hcl.core.type import HclType
from py_hcl.core.type.uint import UIntT


class Add(object):
    def __init__(self, left, right):
        self.left = left
        self.right = right


@hcl_operation('+')
def do_add(left, right):
    return Adder.add(left, right)


class Adder(object):
    t_map = {}

    @classmethod
    def add(cls, lf, rt):
        try:
            return cls.t_map[(type(lf.hcl_type), type(rt.hcl_type))](lf, rt)
        except KeyError:
            raise ExprError.add(lf, rt)

    @staticmethod
    def def_add(lT, rT):
        def f(func):
            Adder.t_map[(lT, rT)] = func
            return func

        return f


@Adder.def_add(UIntT, UIntT)
def _(lf: UIntT, rt: UIntT):
    pass


@Adder.def_add(HclType, HclType)
def _(lf, rt):
    return ExprPlace(HclType, HclExpr())
