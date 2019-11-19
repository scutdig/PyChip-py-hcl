from py_hcl.firrtl_ir.expr.prim_ops import Shr
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
                    return OpCase(Shr) \
                        .arg_types(*arg_types) \
                        .const_arg_types(*const_types) \
                        .res_type(res_type)

            return B

    return A


shr_basis_cases = [
    args(UIntType).const(int).tpe(lambda x, y: uw(max(1, width(x) - y))),
    args(SIntType).const(int).tpe(lambda x, y: sw(max(1, width(x) - y))),
]

shr_type_wrong_cases = [
    args(UnknownType).const(int).tpe(lambda x, y: uw(max(1, y))),
    args(VectorType).const(int).tpe(lambda x, y: uw(max(1, y))),
    args(BundleType).const(int).tpe(lambda x, y: uw(max(1, y))),
]

shr_width_wrong_cases = [
    args(UIntType).const(int).tpe(lambda x, y: uw(max(1, width(x) - y) + 1)),
    args(SIntType).const(int).tpe(lambda x, y: sw(max(1, width(x) - y) + 1)),
    args(UIntType).const(int).tpe(lambda x, y: uw(max(1, width(x) - y) - 1)),
    args(SIntType).const(int).tpe(lambda x, y: sw(max(1, width(x) - y) - 1)),
]


def test_shr():
    basis_tester(shr_basis_cases)
    encounter_error_tester(shr_type_wrong_cases)
    encounter_error_tester(shr_width_wrong_cases)
    serialize_equal(Shr(u(20, w(5)), 3, uw(2)),
                    'shr(UInt<5>("14"), 3)')
    serialize_equal(Shr(s(-20, w(6)), 3, uw(3)),
                    'shr(SInt<6>("-14"), 3)')
