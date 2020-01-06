from py_hcl.firrtl_ir.expr.prim_ops import Add
from py_hcl.firrtl_ir.shortcuts import uw, sw, u, w, s
from py_hcl.firrtl_ir.type import UIntType, SIntType
from tests.test_firrtl_ir.utils import serialize_equal
from .helper import OpCase, basis_tester, \
    encounter_error_tester, type_wrong_cases_2_args_gen, max_width


def args(*arg_types):
    class C:
        @staticmethod
        def tpe(res_type):
            return OpCase(Add).arg_types(*arg_types).res_type(res_type)

    return C


add_basis_cases = [
    args(UIntType, UIntType).tpe(lambda x, y: uw(max_width(x, y) + 1)),
    args(SIntType, SIntType).tpe(lambda x, y: sw(max_width(x, y) + 1)),
]

add_type_wrong_cases = type_wrong_cases_2_args_gen(Add)

add_width_wrong_cases = [
    args(UIntType, UIntType).tpe(lambda x, y: uw(max_width(x, y))),
    args(SIntType, SIntType).tpe(lambda x, y: sw(max_width(x, y))),
    args(UIntType, UIntType).tpe(lambda x, y: uw(max_width(x, y) + 2)),
    args(SIntType, SIntType).tpe(lambda x, y: sw(max_width(x, y) + 2)),
    args(UIntType, UIntType).tpe(lambda x, y: uw(max_width(x, y) - 1)),
    args(SIntType, SIntType).tpe(lambda x, y: sw(max_width(x, y) - 1)),
    args(UIntType, UIntType).tpe(lambda x, y: uw(1)),
    args(SIntType, SIntType).tpe(lambda x, y: sw(1)),
]


def test_add():
    basis_tester(add_basis_cases)
    encounter_error_tester(add_type_wrong_cases)
    encounter_error_tester(add_width_wrong_cases)
    serialize_equal(Add([u(20, w(5)), u(15, w(4))], uw(6)),
                    'add(UInt<5>("h14"), UInt<4>("hf"))')
    serialize_equal(Add([s(-20, w(6)), s(-15, w(5))], sw(6)),
                    'add(SInt<6>("h-14"), SInt<5>("h-f"))')
