from py_hcl.firrtl_ir.expr.prim_ops import Dshl
from py_hcl.firrtl_ir.shortcuts import uw, sw, u, w, s
from py_hcl.firrtl_ir.type import UIntType, SIntType
from tests.test_firrtl_ir.utils import serialize_equal
from .helper import OpCase, basis_tester, \
    encounter_error_tester, type_wrong_cases_2_args_gen, width


def args(*arg_types):
    class C:
        @staticmethod
        def tpe(res_type):
            return OpCase(Dshl).arg_types(*arg_types).res_type(res_type)

    return C


dshl_basis_cases = [
    args(UIntType, UIntType).tpe(
        lambda x, y: uw(width(x) + pow(2, width(y)) - 1)),
    args(SIntType, UIntType).tpe(
        lambda x, y: sw(width(x) + pow(2, width(y)) - 1)),
]

dshl_type_wrong_cases = type_wrong_cases_2_args_gen(Dshl)

dshl_width_wrong_cases = [
    args(UIntType, UIntType).tpe(
        lambda x, y: uw(width(x) + pow(2, width(y)))),
    args(SIntType, UIntType).tpe(
        lambda x, y: sw(width(x) + pow(2, width(y)))),
    args(UIntType, UIntType).tpe(
        lambda x, y: uw(width(x) + pow(2, width(y)) - 2)),
    args(SIntType, UIntType).tpe(
        lambda x, y: sw(width(x) + pow(2, width(y)) - 2)),
]


def test_dshl():
    basis_tester(dshl_basis_cases)
    encounter_error_tester(dshl_type_wrong_cases)
    encounter_error_tester(dshl_width_wrong_cases)
    serialize_equal(Dshl([u(20, w(5)), u(15, w(4))], uw(20)),
                    'dshl(UInt<5>("h14"), UInt<4>("hf"))')
    serialize_equal(Dshl([s(-20, w(6)), u(15, w(4))], uw(21)),
                    'dshl(SInt<6>("h-14"), UInt<4>("hf"))')
