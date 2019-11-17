from py_hcl.firrtl_ir.expr.prim_ops import Add
from py_hcl.firrtl_ir.shortcuts import uw, sw
from py_hcl.firrtl_ir.type import UIntType, SIntType, VectorType, \
    BundleType, UnknownType
from .helper import OpCase, basis_tester, encounter_error_tester


def max_width(x, y):
    return max(x.tpe.width.width, y.tpe.width.width)


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

add_type_wrong_cases = [
    args(UnknownType, UnknownType).tpe(lambda x, y: uw(32)),
    args(UnknownType, UIntType).tpe(lambda x, y: uw(32)),
    args(UnknownType, SIntType).tpe(lambda x, y: sw(32)),
    args(UnknownType, VectorType).tpe(lambda x, y: sw(32)),
    args(UIntType, VectorType).tpe(lambda x, y: uw(32)),
    args(UIntType, BundleType).tpe(lambda x, y: uw(32)),
    args(UIntType, UnknownType).tpe(lambda x, y: uw(32)),
    args(SIntType, VectorType).tpe(lambda x, y: sw(32)),
    args(SIntType, BundleType).tpe(lambda x, y: sw(32)),
    args(SIntType, UnknownType).tpe(lambda x, y: sw(32)),
    args(VectorType, UIntType).tpe(lambda x, y: uw(32)),
    args(VectorType, SIntType).tpe(lambda x, y: sw(32)),
    args(VectorType, VectorType).tpe(lambda x, y: uw(32)),
    args(VectorType, BundleType).tpe(lambda x, y: uw(32)),
    args(BundleType, UIntType).tpe(lambda x, y: uw(32)),
    args(BundleType, SIntType).tpe(lambda x, y: uw(32)),
    args(BundleType, VectorType).tpe(lambda x, y: uw(32)),
    args(BundleType, UnknownType).tpe(lambda x, y: uw(32)),
    args(BundleType, BundleType).tpe(lambda x, y: uw(32)),
]

add_width_wrong_cases = [
    args(UIntType, UIntType).tpe(lambda x, y: uw(max_width(x, y))),
    args(SIntType, SIntType).tpe(lambda x, y: sw(max_width(x, y))),
    args(UIntType, UIntType).tpe(lambda x, y: uw(max_width(x, y) - 1)),
    args(SIntType, SIntType).tpe(lambda x, y: sw(max_width(x, y) - 1)),
    args(SIntType, SIntType).tpe(lambda x, y: sw(1)),
]


def test_add():
    basis_tester(add_basis_cases)
    encounter_error_tester(add_type_wrong_cases)
    encounter_error_tester(add_width_wrong_cases)
