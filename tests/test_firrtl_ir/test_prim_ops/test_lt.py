from py_hcl.firrtl_ir.expr.prim_ops import Lt
from py_hcl.firrtl_ir.shortcuts import uw, sw, u, w, s
from py_hcl.firrtl_ir.type import UIntType, SIntType
from tests.test_firrtl_ir.utils import serialize_equal
from .helper import OpCase, basis_tester, \
    encounter_error_tester, type_wrong_cases_2_args_gen


def args(*arg_types):
    class C:
        @staticmethod
        def tpe(res_type):
            return OpCase(Lt).arg_types(*arg_types).res_type(res_type)

    return C


lt_basis_cases = [
    args(UIntType, UIntType).tpe(lambda x, y: uw(1)),
    args(SIntType, SIntType).tpe(lambda x, y: uw(1)),
]

lt_type_wrong_cases = type_wrong_cases_2_args_gen(Lt) + [
    args(UIntType, UIntType).tpe(lambda x, y: sw(1)),
    args(SIntType, SIntType).tpe(lambda x, y: sw(1)),
]

lt_width_wrong_cases = [
    args(UIntType, UIntType).tpe(lambda x, y: uw(2)),
    args(SIntType, SIntType).tpe(lambda x, y: uw(2)),
    args(UIntType, UIntType).tpe(lambda x, y: uw(3)),
    args(SIntType, SIntType).tpe(lambda x, y: uw(3)),
]


def test_lt():
    basis_tester(lt_basis_cases)
    encounter_error_tester(lt_type_wrong_cases)
    encounter_error_tester(lt_width_wrong_cases)
    serialize_equal(Lt([u(20, w(5)), u(15, w(4))], uw(1)),
                    'lt(UInt<5>("h14"), UInt<4>("hf"))')
    serialize_equal(Lt([s(-20, w(6)), s(-15, w(5))], uw(1)),
                    'lt(SInt<6>("h-14"), SInt<5>("h-f"))')
