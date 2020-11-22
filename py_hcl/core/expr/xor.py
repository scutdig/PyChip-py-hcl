"""
Implement xor operation for pyhcl values.

Examples
--------

>>> from py_hcl import U, S, Wire, Bundle


Xor two literals of Uint type:

>>> res = U(1) ^ U(2)


Xor two literals of Sint type:

>>> res = S(1) ^ S(2)


Xor two wires of Uint type:

>>> w1 = Wire(U.w(8)); w2 = Wire(U.w(9))
>>> res = w1 ^ w2


Xor two wires of Vector type:

>>> w1 = Wire(U.w(8)[8]); w2 = Wire(U.w(9)[8])
>>> res = w1 ^ w2


Xor two wires of Bundle type:

>>> w1 = Wire(Bundle(a=U.w(2), b=~S.w(3)))
>>> w2 = Wire(Bundle(a=U.w(3), b=~S.w(4)))
>>> res = w1 ^ w2
"""

from py_hcl.core.expr import ExprHolder
from py_hcl.core.expr.bundle_holder import BundleHolder
from py_hcl.core.expr.error import ExprError
from py_hcl.core.expr.utils import ensure_all_args_are_values
from py_hcl.core.expr.vec_holder import VecHolder
from py_hcl.core.hcl_ops import op_register
from py_hcl.core.stmt.connect import VariableType
from py_hcl.core.type import HclType
from py_hcl.core.type.bundle import BundleT, Dir
from py_hcl.core.type.sint import SIntT
from py_hcl.core.type.uint import UIntT
from py_hcl.core.type.vector import VectorT
from py_hcl.utils.serialization import json_serialize


@json_serialize
class Xor(object):
    def __init__(self, left, right):
        self.operation = 'xor'
        self.left_expr_id = left.id
        self.right_expr_id = right.id


xorer = op_register('^')


@xorer(UIntT, UIntT)
@ensure_all_args_are_values
def _(lf, rt):
    w = max(lf.hcl_type.width, rt.hcl_type.width)
    t = UIntT(w)
    return ExprHolder(t, VariableType.VALUE, Xor(lf, rt))


@xorer(SIntT, SIntT)
@ensure_all_args_are_values
def _(lf, rt):
    w = max(lf.hcl_type.width, rt.hcl_type.width)
    t = UIntT(w)
    return ExprHolder(t, VariableType.VALUE, Xor(lf, rt))


@xorer(VectorT, VectorT)
@ensure_all_args_are_values
def _(lf, rt):
    # TODO: Accurate Error Message
    assert lf.hcl_type.size == rt.hcl_type.size

    values = [lf[i] ^ rt[i] for i in range(lf.hcl_type.size)]
    v_type = VectorT(values[0].hcl_type, len(values))
    return VecHolder(v_type, VariableType.VALUE, values)


@xorer(BundleT, BundleT)
@ensure_all_args_are_values
def _(lf, rt):
    # TODO: Accurate Error Message
    assert set(lf.hcl_type.fields.keys()) == set(rt.hcl_type.fields.keys())

    bd_type_fields = {}
    bd_values = {}
    for k in lf.hcl_type.fields.keys():
        res = getattr(lf, k) ^ getattr(rt, k)
        bd_type_fields[k] = {"dir": Dir.SRC, "hcl_type": res.hcl_type}
        bd_values[k] = res

    return BundleHolder(BundleT(bd_type_fields), VariableType.VALUE, bd_values)


@xorer(HclType, HclType)
def _(_0, _1):
    raise ExprError.op_type_err('xor', _0, _1)
