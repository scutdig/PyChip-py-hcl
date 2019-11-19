from py_hcl.firrtl_ir.expr.prim_ops import Dshr
from py_hcl.firrtl_ir.shortcuts import uw, sw, u, w, s
from py_hcl.firrtl_ir.type import UIntType, SIntType
from tests.test_firrtl_ir.utils import serialize_equal
from .helper import OpCase, basis_tester, \
    encounter_error_tester, type_wrong_cases_2_args_gen, width


def args(*arg_types):
    class C:
        @staticmethod
        def tpe(res_type):
            return OpCase(Dshr).arg_types(*arg_types).res_type(res_type)

    return C


dshr_basis_cases = [
    args(UIntType, UIntType).tpe(
        lambda x, y: uw(width(x))),
    args(SIntType, UIntType).tpe(
        lambda x, y: sw(width(x))),
]

dshr_type_wrong_cases = type_wrong_cases_2_args_gen(Dshr)

dshr_width_wrong_cases = [
    args(UIntType, UIntType).tpe(
        lambda x, y: uw(width(x) + 1)),
    args(SIntType, UIntType).tpe(
        lambda x, y: sw(width(x) + 1)),
    args(UIntType, UIntType).tpe(
        lambda x, y: uw(width(x) - 1)),
    args(SIntType, UIntType).tpe(
        lambda x, y: sw(width(x) - 1)),
]


def test_dshr():
    basis_tester(dshr_basis_cases)
    encounter_error_tester(dshr_type_wrong_cases)
    encounter_error_tester(dshr_width_wrong_cases)
    serialize_equal(Dshr([u(20, w(5)), u(15, w(4))], uw(5)),
                    'dshr(UInt<5>("14"), UInt<4>("f"))')
    serialize_equal(Dshr([s(-20, w(6)), u(15, w(4))], uw(6)),
                    'dshr(SInt<6>("-14"), UInt<4>("f"))')
