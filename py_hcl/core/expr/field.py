from py_hcl.core.expr import ExprHolder
from py_hcl.core.expr.error import ExprError
from py_hcl.core.hcl_ops import op_register
from py_hcl.core.stmt.connect import ConnSide
from py_hcl.core.type import HclType
from py_hcl.core.type.bundle import BundleT, Dir
from py_hcl.utils import auto_repr

field_accessor = op_register('.')


@auto_repr
class FieldAccess(object):
    def __init__(self, expr, item):
        self.item = item
        self.expr = expr


@field_accessor(BundleT)
def _(bd, item):
    # TODO: Accurate Error Message
    assert item in bd.hcl_type.types
    sd = bd.conn_side
    dr, tpe = bd.hcl_type.types[item]
    new_sd = con_new_sd(sd, dr)
    return ExprHolder(tpe, new_sd, FieldAccess(bd, item))


@field_accessor(HclType)
def _(o, *_):
    raise ExprError.op_type_err('field_accessor', o)


def con_new_sd(sd: ConnSide, dr: Dir) -> ConnSide:
    if sd == ConnSide.BOTH:
        return ConnSide.BOTH
    if sd == ConnSide.RT and dr == dr.SINK:
        return ConnSide.LF
    if sd == ConnSide.LF and dr == dr.SRC:
        return ConnSide.LF
    return ConnSide.RT
