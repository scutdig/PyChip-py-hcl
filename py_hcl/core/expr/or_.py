from py_hcl.core.expr import ExprHolder
from py_hcl.core.expr.bundle_holder import BundleHolder
from py_hcl.core.expr.error import ExprError
from py_hcl.core.expr.utils import assert_right_side
from py_hcl.core.expr.vec_holder import VecHolder
from py_hcl.core.hcl_ops import op_register
from py_hcl.core.stmt.connect import ConnSide
from py_hcl.core.type import HclType
from py_hcl.core.type.bundle import BundleT, Dir
from py_hcl.core.type.sint import SIntT
from py_hcl.core.type.uint import UIntT
from py_hcl.core.type.vector import VectorT
from py_hcl.utils import json_serialize


@json_serialize
class Or(object):
    def __init__(self, left, right):
        self.operation = 'or'
        self.left_expr_id = left.id
        self.right_expr_id = right.id


orer = op_register('|')


@orer(UIntT, UIntT)
@assert_right_side
def _(lf, rt):
    w = max(lf.hcl_type.width, rt.hcl_type.width)
    t = UIntT(w)
    return ExprHolder(t, ConnSide.RT, Or(lf, rt))


@orer(SIntT, SIntT)
@assert_right_side
def _(lf, rt):
    w = max(lf.hcl_type.width, rt.hcl_type.width)
    t = UIntT(w)
    return ExprHolder(t, ConnSide.RT, Or(lf, rt))


@orer(VectorT, VectorT)
@assert_right_side
def _(lf, rt):
    # TODO: Accurate Error Message
    assert lf.hcl_type.size == rt.hcl_type.size

    values = [lf[i] | rt[i] for i in range(lf.hcl_type.size)]
    v_type = VectorT(values[0].hcl_type, len(values))
    return VecHolder(v_type, ConnSide.RT, values)


@orer(BundleT, BundleT)
@assert_right_side
def _(lf, rt):
    # TODO: Accurate Error Message
    assert set(lf.hcl_type.fields.keys()) == set(rt.hcl_type.fields.keys())

    bd_type_fields = {}
    bd_values = {}
    for k in lf.hcl_type.fields.keys():
        res = getattr(lf, k) | getattr(rt, k)
        bd_type_fields[k] = {"dir": Dir.SRC, "hcl_type": res.hcl_type}
        bd_values[k] = res

    return BundleHolder(BundleT(bd_type_fields), ConnSide.RT, bd_values)


@orer(HclType, HclType)
def _(_0, _1):
    raise ExprError.op_type_err('or', _0, _1)
