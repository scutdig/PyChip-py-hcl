from ..type_measurer import equal
from ..type import BundleType, VectorType, UIntType
from .utils import type_in
from ..expr.accessor import SubField, SubIndex, SubAccess


class AccessorTypeChecker(object):
    accessor_checker_map = {}

    @staticmethod
    def check(op_obj):
        try:
            return AccessorTypeChecker.accessor_checker_map[type(op_obj)](
                op_obj
            )
        except KeyError:
            raise NotImplementedError(type(op_obj))


def checker(accessor):
    def f(func):
        AccessorTypeChecker.accessor_checker_map[accessor] = func
        return func

    return f


@checker(SubField)
def _(sub_field):
    from . import check

    if not type_in(sub_field.bundle_ref.tpe, BundleType):
        return False

    if not check(sub_field.bundle_ref):
        return False

    field = None
    for f in sub_field.bundle_ref.tpe.fields:
        if f.name == sub_field.name:
            field = f
            break

    if field is None:
        return False

    if field.is_flipped == sub_field.is_left_value:
        return False

    if not equal(field.tpe, sub_field.tpe):
        return False

    return True


@checker(SubIndex)
def _(sub_index):
    from . import check
    if not check(sub_index.vector_ref):
        return False

    if not type_in(sub_index.vector_ref.tpe, VectorType):
        return False

    if sub_index.vector_ref.tpe.size >= sub_index.index:
        return False

    if not equal(sub_index.vector_ref.tpe.elem_type, sub_index.tpe):
        return False

    return True


@checker(SubAccess)
def _(sub_access):
    from . import check_all
    if not check_all(sub_access.vector_ref, sub_access.index_ref):
        return False

    if not type_in(sub_access.vector_ref.tpe, VectorType):
        return False

    if not type_in(sub_access.index_ref.tpe, UIntType):
        return False

    if not equal(sub_access.vector_ref.tpe.elem_type, sub_access.tpe):
        return False

    return True
