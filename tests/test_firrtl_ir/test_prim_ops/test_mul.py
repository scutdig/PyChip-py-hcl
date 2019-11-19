from py_hcl.firrtl_ir.expr.prim_ops import Mul
from py_hcl.firrtl_ir.shortcuts import uw, sw, u, w, s
from py_hcl.firrtl_ir.type import UIntType, SIntType
from tests.test_firrtl_ir.utils import serialize_equal
from .helper import OpCase, basis_tester, \
    encounter_error_tester, type_wrong_cases_2_args_gen, sum_width


def args(*arg_types):
    class C:
        @staticmethod
        def tpe(res_type):
            return OpCase(Mul).arg_types(*arg_types).res_type(res_type)

    return C


mul_basis_cases = [
    args(UIntType, UIntType).tpe(lambda x, y: uw(sum_width(x, y))),
    args(SIntType, SIntType).tpe(lambda x, y: sw(sum_width(x, y))),
]

mul_type_wrong_cases = type_wrong_cases_2_args_gen(Mul)

mul_width_wrong_cases = [
    args(UIntType, UIntType).tpe(lambda x, y: uw(sum_width(x, y) + 1)),
    args(SIntType, SIntType).tpe(lambda x, y: sw(sum_width(x, y) + 1)),
    args(UIntType, UIntType).tpe(lambda x, y: uw(sum_width(x, y) - 1)),
    args(SIntType, SIntType).tpe(lambda x, y: sw(sum_width(x, y) - 1)),
    args(UIntType, UIntType).tpe(lambda x, y: uw(1)),
    args(SIntType, SIntType).tpe(lambda x, y: sw(1)),
]


def test_mul():
    basis_tester(mul_basis_cases)
    encounter_error_tester(mul_type_wrong_cases)
    encounter_error_tester(mul_width_wrong_cases)
    serialize_equal(Mul([u(20, w(5)), u(15, w(4))], uw(9)),
                    'mul(UInt<5>("14"), UInt<4>("f"))')
    serialize_equal(Mul([s(-20, w(6)), s(-15, w(5))], sw(11)),
                    'mul(SInt<6>("-14"), SInt<5>("-f"))')
