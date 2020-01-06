from py_hcl.firrtl_ir.expr.prim_ops import AsSInt
from py_hcl.firrtl_ir.shortcuts import sw, uw, u, w, s, n
from py_hcl.firrtl_ir.type import UIntType, SIntType, ClockType
from tests.test_firrtl_ir.utils import serialize_equal
from .helper import OpCase, basis_tester, \
    encounter_error_tester, type_wrong_cases_1_arg_gen, width


def args(*arg_types):
    class C:
        @staticmethod
        def tpe(res_type):
            return OpCase(AsSInt).arg_types(*arg_types).res_type(res_type)

    return C


assint_basis_cases = [
    args(UIntType).tpe(lambda x: sw(width(x))),
    args(SIntType).tpe(lambda x: sw(width(x))),
    args(ClockType).tpe(lambda x: sw(1)),
]

assint_type_wrong_cases = type_wrong_cases_1_arg_gen(AsSInt) + [
    args(UIntType).tpe(lambda x: uw(width(x))),
    args(SIntType).tpe(lambda x: uw(width(x))),
    args(ClockType).tpe(lambda x: uw(1)),
]

assint_width_wrong_cases = [
    args(UIntType).tpe(lambda x: sw(width(x) + 1)),
    args(SIntType).tpe(lambda x: sw(width(x) + 1)),
    args(UIntType).tpe(lambda x: sw(width(x) - 1)),
    args(SIntType).tpe(lambda x: sw(width(x) - 1)),
    args(ClockType).tpe(lambda x: sw(2)),
]


def test_assint():
    basis_tester(assint_basis_cases)
    encounter_error_tester(assint_type_wrong_cases)
    encounter_error_tester(assint_width_wrong_cases)
    serialize_equal(AsSInt(u(20, w(5)), sw(5)),
                    'asSInt(UInt<5>("h14"))')
    serialize_equal(AsSInt(s(-20, w(6)), sw(5)),
                    'asSInt(SInt<6>("h-14"))')
    serialize_equal(AsSInt(n("clock", ClockType()), sw(1)),
                    'asSInt(clock)')
