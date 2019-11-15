from py_hcl.firrtl_ir.literal import UIntLiteral
from py_hcl.firrtl_ir.prim_call import PrimCall
from py_hcl.firrtl_ir.prim_ops import Add, Sub, Lt, Leq, \
    Gt, Geq, Eq, Neq, And, Or, Xor
from py_hcl.firrtl_ir.reference import Reference
from py_hcl.firrtl_ir.tpe import UIntType
from py_hcl.firrtl_ir.width import IntWidth
from .utils import serialize_equal


def test_prim_op_add_sub_lt_leq_gt_geq_eq_neq_and_or_xor():
    tpe = UIntType(IntWidth(8))
    ops = [
        Add,
        Sub,
        Lt,
        Leq,
        Gt,
        Geq,
        Eq,
        Neq,
        And,
        Or,
        Xor,
    ]
    cases = [
        ([Reference("a", tpe), Reference("b", tpe)], tpe,
         lambda op: op + '(a, b)'),
        ([UIntLiteral(2, IntWidth(8)), UIntLiteral(4, IntWidth(8))], tpe,
         lambda op: op + '(UInt<8>("2"), UInt<8>("4"))'),
        ([UIntLiteral(2, IntWidth(8)), Reference("a", tpe)], tpe,
         lambda op: op + '(UInt<8>("2"), a)'),
    ]
    for case in cases:
        for o in ops:
            serialize_equal(PrimCall(o, case[0], [], case[1]), case[2](o))
