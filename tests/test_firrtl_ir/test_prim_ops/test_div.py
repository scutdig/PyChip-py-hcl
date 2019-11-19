from py_hcl.firrtl_ir.expr.prim_ops import Div
from py_hcl.firrtl_ir.shortcuts import uw, sw, u, w, s
from py_hcl.firrtl_ir.type import UIntType, SIntType
from tests.test_firrtl_ir.utils import serialize_equal
from .helper import OpCase, basis_tester, \
    encounter_error_tester, type_wrong_cases_2_args_gen, width


def args(*arg_types):
    class C:
        @staticmethod
        def tpe(res_type):
            return OpCase(Div).arg_types(*arg_types).res_type(res_type)

    return C


div_basis_cases = [
    args(UIntType, UIntType).tpe(lambda x, y: uw(width(x))),
    args(SIntType, SIntType).tpe(lambda x, y: sw(width(x) + 1)),
]

div_type_wrong_cases = type_wrong_cases_2_args_gen(Div)

div_width_wrong_cases = [
    args(UIntType, UIntType).tpe(lambda x, y: uw(width(x) + 1)),
    args(SIntType, SIntType).tpe(lambda x, y: sw(width(x) + 2)),
    args(UIntType, UIntType).tpe(lambda x, y: uw(width(x) - 1)),
    args(SIntType, SIntType).tpe(lambda x, y: sw(width(x))),
    args(SIntType, SIntType).tpe(lambda x, y: sw(1)),
]


def test_div():
    basis_tester(div_basis_cases)
    encounter_error_tester(div_type_wrong_cases)
    encounter_error_tester(div_width_wrong_cases)
    serialize_equal(Div([u(20, w(5)), u(15, w(4))], uw(5)),
                    'div(UInt<5>("14"), UInt<4>("f"))')
    serialize_equal(Div([s(-20, w(6)), s(-15, w(5))], uw(7)),
                    'div(SInt<6>("-14"), SInt<5>("-f"))')
