from py_hcl.core.expr import ExprHolder
from py_hcl.core.expr.utils import ensure_all_args_are_readable
from py_hcl.core.hcl_ops import op_register
from py_hcl.core.stmt.connect import VariableType
from py_hcl.core.type.sint import SIntT
from py_hcl.core.type.uint import UIntT
from py_hcl.utils.serialization import json_serialize

extend = op_register('extend')


@json_serialize
class Extend(object):
    def __init__(self, expr):
        self.operation = 'extend'
        self.ref_expr_id = expr.id


@extend(UIntT)
@ensure_all_args_are_readable
def _(uint, size):
    return ExprHolder(UIntT(size), VariableType.ReadOnly, Extend(uint))


@extend(SIntT)
@ensure_all_args_are_readable
def _(sint, size):
    return ExprHolder(SIntT(size), VariableType.ReadOnly, Extend(sint))
