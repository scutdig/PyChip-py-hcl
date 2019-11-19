from py_hcl.firrtl_ir.expr.prim_ops import Or
from py_hcl.firrtl_ir.shortcuts import uw, u, w, s
from py_hcl.firrtl_ir.type import UIntType, SIntType
from tests.test_firrtl_ir.utils import serialize_equal
from .helper import OpCase, basis_tester, \
    encounter_error_tester, type_wrong_cases_2_args_gen, max_width


def args(*arg_types):
    class C:
        @staticmethod
        def tpe(res_type):
            return OpCase(Or).arg_types(*arg_types).res_type(res_type)

    return C


or_basis_cases = [
    args(UIntType, UIntType).tpe(lambda x, y: uw(max_width(x, y))),
    args(SIntType, SIntType).tpe(lambda x, y: uw(max_width(x, y))),
]

or_type_wrong_cases = type_wrong_cases_2_args_gen(Or)

or_width_wrong_cases = [
    args(UIntType, UIntType).tpe(lambda x, y: uw(max_width(x, y) + 1)),
    args(SIntType, SIntType).tpe(lambda x, y: uw(max_width(x, y) + 1)),
    args(UIntType, UIntType).tpe(lambda x, y: uw(max_width(x, y) - 1)),
    args(SIntType, SIntType).tpe(lambda x, y: uw(max_width(x, y) - 1)),
]


def test_or():
    basis_tester(or_basis_cases)
    encounter_error_tester(or_type_wrong_cases)
    encounter_error_tester(or_width_wrong_cases)
    serialize_equal(Or([u(20, w(5)), u(15, w(4))], uw(5)),
                    'or(UInt<5>("14"), UInt<4>("f"))')
    serialize_equal(Or([s(-20, w(6)), s(-15, w(5))], uw(6)),
                    'or(SInt<6>("-14"), SInt<5>("-f"))')
