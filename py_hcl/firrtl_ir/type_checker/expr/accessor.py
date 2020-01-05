import logging

from multipledispatch import dispatch

from ...expr.accessor import SubField, SubIndex, SubAccess
from ...type import BundleType, VectorType, UIntType
from ...type_checker.utils import type_in
from ...type_measurer import equal

checker = dispatch


###############################################################
#                      TYPE CHECKERS                          #
###############################################################

@checker(SubField)
def check(sub_field):
    from .. import check_all_expr
    if not check_all_expr(sub_field.bundle_ref):
        logging.error("sub_field: reference check failed - {}".format(
            sub_field.bundle_ref
        ))
        return False

    if not type_in(sub_field.bundle_ref.tpe, BundleType):
        logging.error("sub_field: reference type check failed - {}".format(
            sub_field.bundle_ref
        ))
        return False

    field = None
    for f in sub_field.bundle_ref.tpe.fields:
        if f.name == sub_field.name:
            field = f
            break
    if field is None:
        logging.error("sub_field: field not exist - {} not in {}".format(
            sub_field.name, sub_field.bundle_ref.tpe.fields
        ))
        return False

    if not equal(field.tpe, sub_field.tpe):
        return False

    return True


@checker(SubIndex)
def check(sub_index):
    from .. import check_all_expr
    if not check_all_expr(sub_index.vector_ref):
        return False

    if not type_in(sub_index.vector_ref.tpe, VectorType):
        return False

    if sub_index.vector_ref.tpe.size <= sub_index.index or sub_index.index < 0:
        return False

    if not equal(sub_index.vector_ref.tpe.elem_type, sub_index.tpe):
        return False

    return True


@checker(SubAccess)
def check(sub_access):
    from .. import check_all_expr
    if not check_all_expr(sub_access.vector_ref, sub_access.index_ref):

        return False

    if not type_in(sub_access.vector_ref.tpe, VectorType):
        return False

    if not type_in(sub_access.index_ref.tpe, UIntType):
        return False

    if not equal(sub_access.vector_ref.tpe.elem_type, sub_access.tpe):
        return False

    return True
