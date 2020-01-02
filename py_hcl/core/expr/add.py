from py_hcl.core.expr import ExprHolder
from py_hcl.core.expr.error import ExprError
from py_hcl.core.expr.utils import assert_right_side
from py_hcl.core.expr.vec_holder import VecHolder
from py_hcl.core.hcl_ops import op_register
from py_hcl.core.stmt.connect import ConnSide
from py_hcl.core.type import HclType
from py_hcl.core.type.sint import SIntT
from py_hcl.core.type.uint import UIntT
from py_hcl.core.type.vector import VectorT
from py_hcl.utils import json_serialize


@json_serialize
class Add(object):
    def __init__(self, left, right):
        self.operation = 'add'
        self.left_expr_id = left.id
        self.right_expr_id = right.id


adder = op_register('+')


@adder(UIntT, UIntT)
@assert_right_side
def _(lf, rt):
    w = max(lf.hcl_type.width, rt.hcl_type.width) + 1
    t = UIntT(w)
    return ExprHolder(t, ConnSide.RT, Add(lf, rt))


@adder(SIntT, SIntT)
@assert_right_side
def _(lf, rt):
    w = max(lf.hcl_type.width, rt.hcl_type.width) + 1
    t = SIntT(w)
    return ExprHolder(t, ConnSide.RT, Add(lf, rt))


@adder(VectorT, VectorT)
@assert_right_side
def _(lf, rt):
    # TODO: Accurate Error Message
    assert lf.hcl_type.size == rt.hcl_type.size

    values = [lf[i] + rt[i] for i in range(lf.hcl_type.size)]
    v_type = VectorT(values[0].hcl_type, len(values))
    return VecHolder(v_type, ConnSide.RT, values)


@adder(HclType, HclType)
def _(_0, _1):
    raise ExprError.op_type_err('add', _0, _1)
