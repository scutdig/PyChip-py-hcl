from py_hcl.firrtl_ir.expr.prim_ops import Rem
from py_hcl.firrtl_ir.shortcuts import uw, sw, u, w, s
from py_hcl.firrtl_ir.type import UIntType, SIntType
from tests.test_firrtl_ir.utils import serialize_equal
from .helper import OpCase, basis_tester, \
    encounter_error_tester, type_wrong_cases_2_args_gen, min_width


def args(*arg_types):
    class C:
        @staticmethod
        def tpe(res_type):
            return OpCase(Rem).arg_types(*arg_types).res_type(res_type)

    return C


rem_basis_cases = [
    args(UIntType, UIntType).tpe(lambda x, y: uw(min_width(x, y))),
    args(SIntType, SIntType).tpe(lambda x, y: sw(min_width(x, y))),
]

rem_type_wrong_cases = type_wrong_cases_2_args_gen(Rem)

rem_width_wrong_cases = [
    args(UIntType, UIntType).tpe(lambda x, y: uw(min_width(x, y) + 1)),
    args(SIntType, SIntType).tpe(lambda x, y: sw(min_width(x, y) + 1)),
    args(UIntType, UIntType).tpe(lambda x, y: uw(min_width(x, y) - 1)),
    args(SIntType, SIntType).tpe(lambda x, y: sw(min_width(x, y) - 1)),
]


def test_rem():
    basis_tester(rem_basis_cases)
    encounter_error_tester(rem_type_wrong_cases)
    encounter_error_tester(rem_width_wrong_cases)
    serialize_equal(Rem([u(20, w(5)), u(15, w(4))], uw(4)),
                    'rem(UInt<5>("h14"), UInt<4>("hf"))')
    serialize_equal(Rem([s(-20, w(6)), s(-15, w(5))], sw(5)),
                    'rem(SInt<6>("h-14"), SInt<5>("h-f"))')
