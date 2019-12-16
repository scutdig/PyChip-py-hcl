from py_hcl.core.expr.error import ExprError
from py_hcl.core.expr.place import ExprPlace
from py_hcl.core.expr import ConnDir
from py_hcl.core.hcl_ops import hcl_operation
from py_hcl.core.type import HclType
from py_hcl.core.type.uint import UIntT
from py_hcl.utils import auto_repr


@auto_repr
class Add(object):
    def __init__(self, left, right):
        self.left = left
        self.right = right


adder = hcl_operation('+')


@adder(UIntT, UIntT)
def _(lf, rt):
    w = max(lf.hcl_type.width, rt.hcl_type.width) + 1
    t = UIntT(w)
    return ExprPlace(t, Add(lf, rt), ConnDir.RT)


@adder(HclType, HclType)
def _(lf, rt):
    # TODO: temporary
    return ExprPlace(HclType(), Add(lf, rt), ConnDir.RT)


@adder(object, object)
def _(lf: object, rt: object):
    raise ExprError.add(lf, rt)
