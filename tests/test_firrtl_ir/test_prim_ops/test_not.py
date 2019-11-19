from py_hcl.firrtl_ir.expr.prim_ops import Not
from py_hcl.firrtl_ir.shortcuts import uw, sw, u, w, s
from py_hcl.firrtl_ir.type import UIntType, SIntType
from tests.test_firrtl_ir.utils import serialize_equal
from .helper import OpCase, basis_tester, \
    encounter_error_tester, type_wrong_cases_1_arg_gen, width


def args(*arg_types):
    class C:
        @staticmethod
        def tpe(res_type):
            return OpCase(Not).arg_types(*arg_types).res_type(res_type)

    return C


not_basis_cases = [
    args(UIntType).tpe(lambda x: uw(width(x))),
    args(SIntType).tpe(lambda x: uw(width(x))),
]

not_type_wrong_cases = type_wrong_cases_1_arg_gen(Not) + [
    args(UIntType).tpe(lambda x: sw(width(x))),
    args(SIntType).tpe(lambda x: sw(width(x))),
]

not_width_wrong_cases = [
    args(UIntType).tpe(lambda x: uw(width(x) + 1)),
    args(SIntType).tpe(lambda x: uw(width(x) + 1)),
    args(UIntType).tpe(lambda x: uw(width(x) - 1)),
    args(SIntType).tpe(lambda x: uw(width(x) - 1)),
]


def test_not():
    basis_tester(not_basis_cases)
    encounter_error_tester(not_type_wrong_cases)
    encounter_error_tester(not_width_wrong_cases)
    serialize_equal(Not(u(20, w(5)), uw(5)),
                    'not(UInt<5>("14"))')
    serialize_equal(Not(s(-20, w(6)), uw(6)),
                    'not(SInt<6>("-14"))')
