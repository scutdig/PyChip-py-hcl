from py_hcl.core.expr import ExprHolder
from py_hcl.core.expr.bundle_holder import BundleHolder
from py_hcl.core.expr.error import ExprError
from py_hcl.core.hcl_ops import op_register
from py_hcl.core.stmt.connect import VariableType
from py_hcl.core.type import HclType
from py_hcl.core.type.bundle import BundleT, Dir
from py_hcl.utils.serialization import json_serialize

field_accessor = op_register('.')


@json_serialize
class FieldAccess(object):
    def __init__(self, expr, item):
        self.operation = "field_access"
        self.item = item
        self.ref_expr_id = expr.id


@field_accessor(BundleT)
def _(bd, item):
    # TODO: Accurate Error Message
    assert item in bd.hcl_type.fields
    if isinstance(bd, BundleHolder):
        return bd.assoc_value[item]

    # build connect side
    var_type = bd.variable_type
    f = bd.hcl_type.fields[item]
    dr, tpe = f["dir"], f["hcl_type"]
    new_var_type = build_new_var_type(var_type, dr)

    return ExprHolder(tpe, new_var_type, FieldAccess(bd, item))


@field_accessor(HclType)
def _(o, *_):
    raise ExprError.op_type_err('field_accessor', o)


def build_new_var_type(var_type: VariableType, dr: Dir) -> VariableType:
    if var_type == VariableType.ASSIGNABLE_VALUE:
        return VariableType.ASSIGNABLE_VALUE
    if var_type == VariableType.VALUE and dr == dr.SINK:
        return VariableType.LOCATION
    if var_type == VariableType.LOCATION and dr == dr.SRC:
        return VariableType.LOCATION
    return VariableType.VALUE
