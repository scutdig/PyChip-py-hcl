from py_hcl.core.expr.place import ExprPlace
from py_hcl.core.expr import ConnDir
from py_hcl.core.hcl_ops import hcl_operation
from py_hcl.core.type.bundle import BundleT, Dir
from py_hcl.utils import auto_repr

field_accessor = hcl_operation('.')


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
    return ExprPlace(tpe, FieldAccess(bd, item), cd)
