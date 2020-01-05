import logging
from enum import Enum

from py_hcl.core.hcl_ops import op_register, op_apply
from py_hcl.core.stmt.error import StatementError
from py_hcl.core.stmt_factory.trapper import StatementTrapper
from py_hcl.core.type import HclType
from py_hcl.core.type.bundle import BundleT, Dir
from py_hcl.core.type.sint import SIntT
from py_hcl.core.type.uint import UIntT
from py_hcl.core.type.vector import VectorT
from py_hcl.utils import json_serialize


class ConnSide(Enum):
    UNKNOWN = 0
    LF = 1
    RT = 2
    BOTH = 3


@json_serialize
class Connect(object):
    def __init__(self, left, right):
        self.stmt_type = 'connect'
        self.left_expr_id = left.id
        self.right_expr_id = right.id


connector = op_register('<<=')


@connector(UIntT, UIntT)
def _(left, right):
    check_connect_dir(left, right)

    if left.hcl_type.width < right.hcl_type.width:
        msg = 'connect(): connecting {} to {} will truncate the bits'.format(
            right.hcl_type, left.hcl_type)
        logging.warning(msg)
        right = right[left.hcl_type.width - 1:0]

    if left.hcl_type.width > right.hcl_type.width:
        right = op_apply('extend')(right, left.hcl_type.width)

    assert left.hcl_type.width == right.hcl_type.width
    StatementTrapper.track(Connect(left, right))
    return left


@connector(SIntT, SIntT)
def _(left, right):
    check_connect_dir(left, right)

    if left.hcl_type.width < right.hcl_type.width:
        logging.warning(
            'connect(): connecting {} to {} will truncate the bits'.format(
                right.hcl_type, left.hcl_type
            ))
        right = right[left.hcl_type.width - 1:0].to_sint()

    if left.hcl_type.width > right.hcl_type.width:
        right = op_apply('extend')(right, left.hcl_type.width)

    assert left.hcl_type.width == right.hcl_type.width
    StatementTrapper.track(Connect(left, right))
    return left


@connector(UIntT, SIntT)
def _(left, right):
    msg = 'connect(): connecting SInt to UInt, an auto-conversion will occur'
    logging.warning(msg)

    if left.hcl_type.width < right.hcl_type.width:
        logging.warning(
            'connect(): connecting {} to {} will truncate the bits'.format(
                right.hcl_type, left.hcl_type
            ))
        return op_apply('<<=')(left, right[left.hcl_type.width - 1:0])

    return op_apply('<<=')(left, right.to_uint())


@connector(SIntT, UIntT)
def _(left, right):
    msg = 'connect(): connecting UInt to SInt, an auto-conversion will occur'
    logging.warning(msg)

    if left.hcl_type.width < right.hcl_type.width:
        logging.warning(
            'connect(): connecting {} to {} will truncate the bits'.format(
                right.hcl_type, left.hcl_type
            ))
        right = right[left.hcl_type.width - 1:0]

    return op_apply('<<=')(left, right.to_sint())


@connector(BundleT, BundleT)
def _(left, right):
    check_connect_dir(left, right)

    # TODO: Accurate Error Message
    dir_and_types = right.hcl_type.fields
    keys = dir_and_types.keys()
    assert keys == left.hcl_type.fields.keys()

    for k in keys:
        lf = op_apply('.')(left, k)
        rt = op_apply('.')(right, k)
        if dir_and_types[k]['dir'] == Dir.SRC:
            op_apply('<<=')(lf, rt)
        else:
            op_apply('<<=')(rt, lf)

    return left


@connector(VectorT, VectorT)
def _(left, right):
    check_connect_dir(left, right)

    # TODO: Accurate Error Message
    assert left.hcl_type.size == right.hcl_type.size

    for i in range(left.hcl_type.size):
        op_apply('<<=')(left[i], right[i])

    return left


@connector(HclType, HclType)
def _(_0, _1):
    raise StatementError.connect_type_error(_0, _1)


def check_connect_dir(left, right):
    # TODO: Accurate Error Message
    assert left.conn_side in (ConnSide.LF, ConnSide.BOTH)
    assert right.conn_side in (ConnSide.RT, ConnSide.BOTH)
