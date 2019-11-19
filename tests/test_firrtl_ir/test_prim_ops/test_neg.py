from py_hcl.firrtl_ir.expr.prim_ops import Neg
from py_hcl.firrtl_ir.shortcuts import sw, uw, u, w, s
from py_hcl.firrtl_ir.type import UIntType, SIntType
from tests.test_firrtl_ir.utils import serialize_equal
from .helper import OpCase, basis_tester, \
    encounter_error_tester, type_wrong_cases_1_arg_gen, width


def args(*arg_types):
    class C:
        @staticmethod
        def tpe(res_type):
            return OpCase(Neg).arg_types(*arg_types).res_type(res_type)

    return C


neg_basis_cases = [
    args(UIntType).tpe(lambda x: sw(width(x) + 1)),
    args(SIntType).tpe(lambda x: sw(width(x) + 1)),
]

neg_type_wrong_cases = type_wrong_cases_1_arg_gen(Neg) + [
    args(UIntType).tpe(lambda x: uw(width(x) + 1)),
    args(SIntType).tpe(lambda x: uw(width(x) + 1)),
]

neg_width_wrong_cases = [
    args(UIntType).tpe(lambda x: sw(width(x) + 2)),
    args(SIntType).tpe(lambda x: sw(width(x) + 2)),
    args(UIntType).tpe(lambda x: sw(width(x))),
    args(SIntType).tpe(lambda x: sw(width(x))),
    args(UIntType).tpe(lambda x: sw(1)),
    args(SIntType).tpe(lambda x: sw(1)),
]


def test_neg():
    basis_tester(neg_basis_cases)
    encounter_error_tester(neg_type_wrong_cases)
    encounter_error_tester(neg_width_wrong_cases)
    serialize_equal(Neg(u(20, w(5)), sw(6)),
                    'neg(UInt<5>("14"))')
    serialize_equal(Neg(s(-20, w(6)), sw(7)),
                    'neg(SInt<6>("-14"))')
