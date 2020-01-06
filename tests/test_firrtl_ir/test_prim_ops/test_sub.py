from py_hcl.firrtl_ir.expr.prim_ops import Sub
from py_hcl.firrtl_ir.shortcuts import sw, u, w, s
from py_hcl.firrtl_ir.type import SIntType, UIntType
from tests.test_firrtl_ir.utils import serialize_equal
from .helper import basis_tester, encounter_error_tester, OpCase, \
    type_wrong_cases_2_args_gen


def max_width(x, y):
    return max(x.tpe.width.width, y.tpe.width.width)


def args(*arg_types):
    class C:
        @staticmethod
        def tpe(res_type):
            return OpCase(Sub).arg_types(*arg_types).res_type(res_type)

    return C


sub_basis_cases = [
    args(UIntType, UIntType).tpe(lambda x, y: sw(max_width(x, y) + 1)),
    args(SIntType, SIntType).tpe(lambda x, y: sw(max_width(x, y) + 1)),
]

sub_type_wrong_cases = type_wrong_cases_2_args_gen(Sub)

sub_width_wrong_cases = [
    args(UIntType, UIntType).tpe(lambda x, y: sw(max_width(x, y))),
    args(SIntType, SIntType).tpe(lambda x, y: sw(max_width(x, y))),
    args(UIntType, UIntType).tpe(lambda x, y: sw(max_width(x, y) + 2)),
    args(SIntType, SIntType).tpe(lambda x, y: sw(max_width(x, y) + 2)),
    args(UIntType, UIntType).tpe(lambda x, y: sw(max_width(x, y) - 1)),
    args(SIntType, SIntType).tpe(lambda x, y: sw(max_width(x, y) - 1)),
    args(UIntType, UIntType).tpe(lambda x, y: sw(1)),
    args(SIntType, SIntType).tpe(lambda x, y: sw(1)),
]


def test_sub():
    basis_tester(sub_basis_cases)
    encounter_error_tester(sub_type_wrong_cases)
    encounter_error_tester(sub_width_wrong_cases)
    serialize_equal(Sub([u(20, w(5)), u(15, w(4))], sw(6)),
                    'sub(UInt<5>("h14"), UInt<4>("hf"))')
    serialize_equal(Sub([s(-20, w(6)), s(-15, w(5))], sw(7)),
                    'sub(SInt<6>("h-14"), SInt<5>("h-f"))')
