from py_hcl.firrtl_ir.expr.prim_ops import Shl
from py_hcl.firrtl_ir.shortcuts import sw, uw, u, w, s
from py_hcl.firrtl_ir.type import BundleType, SIntType, \
    UIntType, UnknownType, VectorType
from tests.test_firrtl_ir.utils import serialize_equal
from .helper import basis_tester, encounter_error_tester, OpCase, width


def args(*arg_types):
    class A:
        @staticmethod
        def const(*const_types):
            class B:
                @staticmethod
                def tpe(res_type):
                    return OpCase(Shl) \
                        .arg_types(*arg_types) \
                        .const_arg_types(*const_types) \
                        .res_type(res_type)

            return B

    return A


shl_basis_cases = [
    args(UIntType).const(int).tpe(lambda x, y: uw(width(x) + y)),
    args(SIntType).const(int).tpe(lambda x, y: sw(width(x) + y)),
]

shl_type_wrong_cases = [
    args(UnknownType).const(int).tpe(lambda x, y: uw(y)),
    args(VectorType).const(int).tpe(lambda x, y: uw(y)),
    args(BundleType).const(int).tpe(lambda x, y: uw(y)),
]

shl_width_wrong_cases = [
    args(UIntType).const(int).tpe(lambda x, y: uw(width(x) + y + 1)),
    args(SIntType).const(int).tpe(lambda x, y: sw(width(x) + y + 1)),
    args(UIntType).const(int).tpe(lambda x, y: uw(width(x) + y - 1)),
    args(SIntType).const(int).tpe(lambda x, y: sw(width(x) + y - 1)),
]


def test_shl():
    basis_tester(shl_basis_cases)
    encounter_error_tester(shl_type_wrong_cases)
    encounter_error_tester(shl_width_wrong_cases)
    serialize_equal(Shl(u(20, w(5)), 6, uw(11)),
                    'shl(UInt<5>("14"), 6)')
    serialize_equal(Shl(s(-20, w(6)), 6, sw(12)),
                    'shl(SInt<6>("-14"), 6)')
