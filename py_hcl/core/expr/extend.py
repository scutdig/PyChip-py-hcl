from py_hcl.core.expr import ExprHolder
from py_hcl.core.expr.utils import assert_right_side
from py_hcl.core.hcl_ops import op_register
from py_hcl.core.stmt.connect import ConnSide
from py_hcl.core.type.sint import SIntT
from py_hcl.core.type.uint import UIntT
from py_hcl.utils import json_serialize

extend = op_register('extend')


@json_serialize
class Extend(object):
    def __init__(self, expr):
        self.operation = 'extend'
        self.ref_expr_id = expr.id


@extend(UIntT)
@assert_right_side
def _(uint, size):
    return ExprHolder(UIntT(size), ConnSide.RT, Extend(uint))


@extend(SIntT)
@assert_right_side
def _(sint, size):
    return ExprHolder(SIntT(size), ConnSide.RT, Extend(sint))
