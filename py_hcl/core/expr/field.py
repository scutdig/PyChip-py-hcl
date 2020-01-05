from py_hcl.core.expr import ExprHolder
from py_hcl.core.expr.bundle_holder import BundleHolder
from py_hcl.core.expr.error import ExprError
from py_hcl.core.hcl_ops import op_register
from py_hcl.core.stmt.connect import ConnSide
from py_hcl.core.type import HclType
from py_hcl.core.type.bundle import BundleT, Dir
from py_hcl.utils import json_serialize

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
    sd = bd.conn_side
    f = bd.hcl_type.fields[item]
    dr, tpe = f["dir"], f["hcl_type"]
    new_sd = build_new_sd(sd, dr)

    return ExprHolder(tpe, new_sd, FieldAccess(bd, item))


@field_accessor(HclType)
def _(o, *_):
    raise ExprError.op_type_err('field_accessor', o)


def build_new_sd(sd: ConnSide, dr: Dir) -> ConnSide:
    if sd == ConnSide.BOTH:
        return ConnSide.BOTH
    if sd == ConnSide.RT and dr == dr.SINK:
        return ConnSide.LF
    if sd == ConnSide.LF and dr == dr.SRC:
        return ConnSide.LF
    return ConnSide.RT
