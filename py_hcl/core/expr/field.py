from py_hcl.core.expr import ExprHolder
from py_hcl.core.stmt.connect import ConnLoc
from py_hcl.core.expr.error import ExprError
from py_hcl.core.hcl_ops import op_register
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
    assert item in bd.hcl_type.types
    dr, tpe = bd.hcl_type.types[item]
    cd = ConnLoc.RT if dr == Dir.SRC else ConnLoc.LF
    return ExprHolder(tpe, cd, FieldAccess(bd, item))


@field_accessor(object)
def _(o, *_):
    raise ExprError.op_type_err('field_accessor', o)
