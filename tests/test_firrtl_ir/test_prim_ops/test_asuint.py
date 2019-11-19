from py_hcl.firrtl_ir.expr.prim_ops import AsUInt
from py_hcl.firrtl_ir.shortcuts import uw, sw, u, w, s, n
from py_hcl.firrtl_ir.type import UIntType, SIntType, ClockType
from tests.test_firrtl_ir.utils import serialize_equal
from .helper import OpCase, basis_tester, \
    encounter_error_tester, type_wrong_cases_1_arg_gen, width


def args(*arg_types):
    class C:
        @staticmethod
        def tpe(res_type):
            return OpCase(AsUInt).arg_types(*arg_types).res_type(res_type)

    return C


asuint_basis_cases = [
    args(UIntType).tpe(lambda x: uw(width(x))),
    args(SIntType).tpe(lambda x: uw(width(x))),
    args(ClockType).tpe(lambda x: uw(1)),
]

asuint_type_wrong_cases = type_wrong_cases_1_arg_gen(AsUInt) + [
    args(UIntType).tpe(lambda x: sw(width(x))),
    args(SIntType).tpe(lambda x: sw(width(x))),
    args(ClockType).tpe(lambda x: sw(1)),
]

asuint_width_wrong_cases = [
    args(UIntType).tpe(lambda x: uw(width(x) + 1)),
    args(SIntType).tpe(lambda x: uw(width(x) + 1)),
    args(UIntType).tpe(lambda x: uw(width(x) - 1)),
    args(SIntType).tpe(lambda x: uw(width(x) - 1)),
    args(ClockType).tpe(lambda x: uw(2)),
]


def test_asuint():
    basis_tester(asuint_basis_cases)
    encounter_error_tester(asuint_type_wrong_cases)
    encounter_error_tester(asuint_width_wrong_cases)
    serialize_equal(AsUInt(u(20, w(5)), uw(5)),
                    'asUInt(UInt<5>("14"))')
    serialize_equal(AsUInt(s(-20, w(6)), uw(5)),
                    'asUInt(SInt<6>("-14"))')
    serialize_equal(AsUInt(n("clock", ClockType()), uw(1)),
                    'asUInt(clock)')
