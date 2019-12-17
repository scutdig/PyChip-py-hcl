from py_hcl.core.expr import ExprHolder
from py_hcl.core.stmt.connect import ConnLoc
from py_hcl.core.expr.error import ExprError
from py_hcl.core.hcl_ops import op_register
from py_hcl.core.type.sint import SIntT
from py_hcl.core.type.uint import UIntT
from py_hcl.utils import auto_repr

slice_ = op_register('[i:j]')
index = op_register('[i]')


@auto_repr
class Bits(object):
    def __init__(self, expr, high, low):
        self.high = high
        self.low = low
        self.expr = expr


@slice_(UIntT)
def _(uint, high: int, low: int):
    check_bit_width(uint, high, low)
    t = UIntT(high - low + 1)
    return ExprHolder(t, ConnLoc.RT, Bits(uint, high, low))


@slice_(SIntT)
def _(sint, high: int, low: int):
    check_bit_width(sint, high, low)
    t = UIntT(high - low + 1)
    return ExprHolder(t, ConnLoc.RT, Bits(sint, high, low))


@slice_(object)
def _(_0, *_):
    ExprError.op_type_err('slice', _0)


@index(UIntT)
def _(uint, i: int):
    return uint[i:i]


@index(SIntT)
def _(sint, i: int):
    return sint[i:i]


@index(object)
def _(_0, *_):
    ExprError.op_type_err('index', _0)


def check_bit_width(uint, high, low):
    w = uint.hcl_type.width
    assert w > high >= low >= 0
