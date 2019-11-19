from py_hcl.firrtl_ir.expr.prim_ops import Neq
from py_hcl.firrtl_ir.shortcuts import uw, sw, u, w, s
from py_hcl.firrtl_ir.type import UIntType, SIntType
from tests.test_firrtl_ir.utils import serialize_equal
from .helper import OpCase, basis_tester, \
    encounter_error_tester, type_wrong_cases_2_args_gen


def args(*arg_types):
    class C:
        @staticmethod
        def tpe(res_type):
            return OpCase(Neq).arg_types(*arg_types).res_type(res_type)

    return C


neq_basis_cases = [
    args(UIntType, UIntType).tpe(lambda x, y: uw(1)),
    args(SIntType, SIntType).tpe(lambda x, y: uw(1)),
]

neq_type_wrong_cases = type_wrong_cases_2_args_gen(Neq) + [
    args(UIntType, UIntType).tpe(lambda x, y: sw(1)),
    args(SIntType, SIntType).tpe(lambda x, y: sw(1)),
]

neq_width_wrong_cases = [
    args(UIntType, UIntType).tpe(lambda x, y: uw(2)),
    args(SIntType, SIntType).tpe(lambda x, y: uw(2)),
    args(UIntType, UIntType).tpe(lambda x, y: uw(3)),
    args(SIntType, SIntType).tpe(lambda x, y: uw(3)),
]


def test_neq():
    basis_tester(neq_basis_cases)
    encounter_error_tester(neq_type_wrong_cases)
    encounter_error_tester(neq_width_wrong_cases)
    serialize_equal(Neq([u(20, w(5)), u(15, w(4))], uw(1)),
                    'neq(UInt<5>("14"), UInt<4>("f"))')
    serialize_equal(Neq([s(-20, w(6)), s(-15, w(5))], uw(1)),
                    'neq(SInt<6>("-14"), SInt<5>("-f"))')
