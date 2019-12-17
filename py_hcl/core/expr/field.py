from py_hcl.core.expr import ConnDir, ExprHolder
from py_hcl.core.expr.error import ExprError
from py_hcl.core.hcl_ops import op_register
from py_hcl.core.type.bundle import BundleT, Dir
from py_hcl.utils import auto_repr

field_accessor = op_register('.')


@auto_repr
class FieldAccess(object):
    def __init__(self, obj, item):
        self.obj = obj
        self.item = item


@field_accessor(BundleT)
def _(bd, item):
    assert item in bd.hcl_type.types
    dr, tpe = bd.hcl_type.types[item]
    cd = ConnDir.RT if dr == Dir.IN else ConnDir.LF
    return ExprHolder(tpe, cd, FieldAccess(bd, item))


@field_accessor(object)
def _(o, *_):
    raise ExprError.op_type_err('field_accessor', o)