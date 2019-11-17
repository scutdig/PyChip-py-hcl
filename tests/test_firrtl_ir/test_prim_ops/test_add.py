from py_hcl.firrtl_ir.expr.prim_ops import Add
from py_hcl.firrtl_ir.shortcuts import uw, sw
from py_hcl.firrtl_ir.type import UIntType, SIntType, VectorType, BundleType
from .helper import OpCase, basis_tester, encounter_error_tester


def max_width(x, y):
    return max(x.tpe.width.width, y.tpe.width.width)


add_basis_cases = [
    OpCase(
        Add
    ).arg_types(
        UIntType, UIntType
    ).res_type(
        lambda x, y: uw(max_width(x, y) + 1)
    ),

    OpCase(
        Add
    ).arg_types(
        SIntType, SIntType
    ).res_type(
        lambda x, y: sw(max_width(x, y) + 1)
    ),
]

add_type_wrong_cases = [
    OpCase(
        Add
    ).arg_types(
        UIntType, VectorType
    ).res_type(
        lambda x, y: uw(5)
    ),

    OpCase(
        Add
    ).arg_types(
        UIntType, BundleType
    ).res_type(
        lambda x, y: uw(5)
    ),

    OpCase(
        Add
    ).arg_types(
        SIntType, VectorType
    ).res_type(
        lambda x, y: sw(5)
    ),

    OpCase(
        Add
    ).arg_types(
        SIntType, BundleType
    ).res_type(
        lambda x, y: sw(5)
    ),
]

add_width_wrong_cases = [
    OpCase(
        Add
    ).arg_types(
        UIntType, UIntType
    ).res_type(
        lambda x, y: uw(max_width(x, y))
    ),

    OpCase(
        Add
    ).arg_types(
        SIntType, SIntType
    ).res_type(
        lambda x, y: sw(max_width(x, y))
    ),
]

basis_tester(add_basis_cases)
encounter_error_tester(add_type_wrong_cases)
encounter_error_tester(add_width_wrong_cases)
