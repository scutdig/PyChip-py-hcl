from py_hcl.core.expr import ExprHolder
from py_hcl.core.expr.bundle_holder import BundleHolder
from py_hcl.core.expr.error import ExprError
from py_hcl.core.hcl_ops import op_register
from py_hcl.core.stmt.connect import VariableType
from py_hcl.core.type import HclType
from py_hcl.core.type.bundle import BundleT, BundleDirection
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


def build_new_var_type(var_type: VariableType,
                       dr: BundleDirection) -> VariableType:
    if var_type == VariableType.ReadWrite:
        return VariableType.ReadWrite
    if var_type == VariableType.ReadOnly and dr == dr.SINK:
        return VariableType.WriteOnly
    if var_type == VariableType.WriteOnly and dr == dr.SOURCE:
        return VariableType.WriteOnly
    return VariableType.ReadOnly
