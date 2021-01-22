from py_hcl.core.expr import ExprHolder
from py_hcl.core.expr.error import ExprError
from py_hcl.core.expr.utils import ensure_all_args_are_readable
from py_hcl.core.expr.vec_holder import VecHolder
from py_hcl.core.hcl_ops import op_register
from py_hcl.core.type import HclType
from py_hcl.core.type.sint import SIntT
from py_hcl.core.type.uint import UIntT
from py_hcl.core.type.vector import VectorT
from py_hcl.utils.serialization import json_serialize

index = op_register('[i]')


@json_serialize
class VecIndex(object):
    def __init__(self, expr, idx: int):
        self.operation = "vec_index"
        self.index = idx
        self.ref_expr_id = expr.id


@index(UIntT)
@ensure_all_args_are_readable
def _(uint, i: int):
    return uint[i:i]


@index(SIntT)
@ensure_all_args_are_readable
def _(sint, i: int):
    return sint[i:i]


@index(VectorT)
def _(vec, i: int):
    # TODO: Accurate Error Message
    assert i < vec.hcl_type.size
    if isinstance(vec, VecHolder):
        return vec.assoc_value[i]
    return ExprHolder(vec.hcl_type.inner_type, vec.variable_type,
                      VecIndex(vec, i))


@index(HclType)
def _(_0, *_):
    raise ExprError.op_type_err('index', _0)
