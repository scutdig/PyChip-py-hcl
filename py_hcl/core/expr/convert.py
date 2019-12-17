from py_hcl.core.expr import ExprHolder
from py_hcl.core.stmt.connect import ConnLoc
from py_hcl.core.hcl_ops import op_register
from py_hcl.core.type.sint import SIntT
from py_hcl.core.type.uint import UIntT
from py_hcl.utils import auto_repr

to_bool = op_register('to_bool')
to_uint = op_register('to_uint')
to_sint = op_register('to_sint')


@auto_repr
class ToSInt(object):
    def __init__(self, expr):
        self.expr = expr


@auto_repr
class ToUInt(object):
    def __init__(self, expr):
        self.expr = expr


@to_bool(UIntT)
def _(uint):
    return uint[0]


@to_bool(SIntT)
def _(sint):
    return sint[0]


@to_uint(UIntT)
def _(uint):
    return uint


@to_uint(SIntT)
def _(sint):
    t = UIntT(sint.hcl_type.width)
    return ExprHolder(t, ConnLoc.RT, ToUInt(sint))


@to_sint(UIntT)
def _(uint):
    t = SIntT(uint.hcl_type.width)
    return ExprHolder(t, ConnLoc.RT, ToSInt(uint))


@to_sint(SIntT)
def _(sint):
    return sint
