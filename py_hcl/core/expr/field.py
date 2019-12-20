from py_hcl.core.expr import ExprHolder
from py_hcl.core.expr.error import ExprError
from py_hcl.core.expr.io import IO, IOHolder
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

    # build connect side
    sd = bd.conn_side
    dr, tpe = bd.hcl_type.types[item]
    new_sd = build_new_sd(sd, dr)

    # for io
    if isinstance(bd, IO):
        bd = fetch_inner_io_holder(bd, item)

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


def fetch_inner_io_holder(io, name) -> IOHolder:
    current_node = io.io_chain_head
    while True:
        if name in current_node.io_holder.named_ports:
            return current_node.io_holder
        current_node = current_node.next_node
