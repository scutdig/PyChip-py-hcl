from py_hcl.firrtl_ir.expr.prim_ops import Bits
from py_hcl.firrtl_ir.shortcuts import uw, u, w, s
from py_hcl.firrtl_ir.type import UIntType, SIntType, \
    UnknownType, VectorType, BundleType
from tests.test_firrtl_ir.utils import serialize_equal
from .helper import OpCase, basis_tester, \
    encounter_error_tester, width


def args(*arg_types):
    class A:
        @staticmethod
        def const(*const_types):
            class B:
                @staticmethod
                def filter(valid_fn):
                    class C:
                        @staticmethod
                        def tpe(res_type):
                            return OpCase(Bits) \
                                .arg_types(*arg_types) \
                                .const_arg_types(*const_types) \
                                .filter(valid_fn) \
                                .res_type(res_type)

                    return C

            return B

    return A


bits_basis_cases = [
    args(UIntType).const(int, int).filter(
        lambda u, a, b: width(u) > a >= b >= 0).tpe(
        lambda u, a, b: uw(a - b + 1)),
    args(SIntType).const(int, int).filter(
        lambda u, a, b: width(u) > a >= b >= 0).tpe(
        lambda u, a, b: uw(a - b + 1)),
]

bits_type_wrong_cases = [
    args(UnknownType).const(int, int).filter(
        lambda u, a, b: a >= b >= 0).tpe(
        lambda u, a, b: uw(a - b + 1)),
    args(VectorType).const(int, int).filter(
        lambda u, a, b: a >= b >= 0).tpe(
        lambda u, a, b: uw(a - b + 1)),
    args(BundleType).const(int, int).filter(
        lambda u, a, b: a >= b >= 0).tpe(
        lambda u, a, b: uw(a - b + 1)),
]

bits_width_wrong_cases = [
    args(UIntType).const(int, int).filter(
        lambda u, a, b: width(u) > a >= b >= 0).tpe(
        lambda u, a, b: uw(a - b + 2)),
    args(SIntType).const(int, int).filter(
        lambda u, a, b: width(u) > a >= b >= 0).tpe(
        lambda u, a, b: uw(a - b + 2)),
    args(UIntType).const(int, int).filter(
        lambda u, a, b: width(u) > a >= b >= 0).tpe(
        lambda u, a, b: uw(a - b)),
    args(SIntType).const(int, int).filter(
        lambda u, a, b: width(u) > a >= b >= 0).tpe(
        lambda u, a, b: uw(a - b)),
]

bits_invalid_cases = [
    args(UIntType).const(int, int).filter(
        lambda u, a, b: width(u) <= a and a >= b >= 0).tpe(
        lambda u, a, b: uw(a - b + 1)),
    args(SIntType).const(int, int).filter(
        lambda u, a, b: width(u) <= a and a >= b >= 0).tpe(
        lambda u, a, b: uw(a - b + 1)),
    args(UIntType).const(int, int).filter(
        lambda u, a, b: width(u) > a and b > a >= 0).tpe(
        lambda u, a, b: uw(b - a + 1)),
    args(SIntType).const(int, int).filter(
        lambda u, a, b: width(u) > a and b > a >= 0).tpe(
        lambda u, a, b: uw(b - a + 1)),
]


def test_bits():
    basis_tester(bits_basis_cases)
    encounter_error_tester(bits_type_wrong_cases)
    encounter_error_tester(bits_width_wrong_cases)
    encounter_error_tester(bits_invalid_cases)
    serialize_equal(Bits(u(20, w(5)), [4, 4], uw(1)),
                    'bits(UInt<5>("h14"), 4, 4)')
    serialize_equal(Bits(s(-20, w(6)), [4, 3], uw(2)),
                    'bits(SInt<6>("h-14"), 4, 3)')
