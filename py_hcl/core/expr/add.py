from py_hcl.core.expr.error import ExprError
from py_hcl.core.expr import ExprHolder
from py_hcl.core.stmt.connect import ConnSide
from py_hcl.core.hcl_ops import op_register
from py_hcl.core.type.sint import SIntT
from py_hcl.core.type.uint import UIntT
from py_hcl.utils import auto_repr


@auto_repr
class Add(object):
    def __init__(self, left, right):
        self.left = left
        self.right = right


adder = op_register('+')


@adder(UIntT, UIntT)
def _(lf, rt):
    check_add_dir(lf, rt)
    w = max(lf.hcl_type.width, rt.hcl_type.width) + 1
    t = UIntT(w)
    return ExprHolder(t, ConnSide.RT, Add(lf, rt))


@adder(SIntT, SIntT)
def _(lf, rt):
    check_add_dir(lf, rt)
    w = max(lf.hcl_type.width, rt.hcl_type.width) + 1
    t = SIntT(w)
    return ExprHolder(t, ConnSide.RT, Add(lf, rt))


@adder(object, object)
def _(_0, _1):
    raise ExprError.op_type_err('add', _0, _1)


def check_add_dir(lf, rt):
    assert lf.conn_side in (ConnSide.RT, ConnSide.BOTH)
    assert rt.conn_side in (ConnSide.RT, ConnSide.BOTH)
