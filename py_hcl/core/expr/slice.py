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

slice_ = op_register('[i:j]')


@json_serialize
class Bits(object):
    def __init__(self, expr, high, low):
        self.operation = 'bits'
        self.high = high
        self.low = low
        self.ref_expr_id = expr.id


@slice_(UIntT)
@assert_right_side
def _(uint, high: int, low: int):
    check_bit_width(uint, high, low)
    t = UIntT(high - low + 1)
    return ExprHolder(t, ConnSide.RT, Bits(uint, high, low))


@slice_(SIntT)
@assert_right_side
def _(sint, high: int, low: int):
    check_bit_width(sint, high, low)
    t = UIntT(high - low + 1)
    return ExprHolder(t, ConnSide.RT, Bits(sint, high, low))


@slice_(VectorT)
def _(vec, low: int, high: int):
    check_vec_size(vec, low, high)

    if isinstance(vec, VecHolder):
        values = vec.assoc_value[low: high]
    else:
        values = [vec[i] for i in range(low, high, 1)]

    v_type = VectorT(vec.hcl_type.inner_type, high - low)
    return VecHolder(v_type, vec.conn_side, values)


@slice_(HclType)
def _(_0, *_):
    ExprError.op_type_err('slice', _0)


def check_bit_width(uint, high, low):
    w = uint.hcl_type.width
    # TODO: Accurate Error Message
    assert w > high >= low >= 0


def check_vec_size(vec, low, high):
    s = vec.hcl_type.size
    # TODO: Accurate Error Message
    assert 0 <= low < high <= s
