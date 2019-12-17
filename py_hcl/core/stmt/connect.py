import logging
from enum import Enum

from py_hcl.core.hcl_ops import op_register, op_apply
from py_hcl.core.stmt.error import StatementError
from py_hcl.core.stmt_factory.trapper import StatementTrapper
from py_hcl.core.type.sint import SIntT
from py_hcl.core.type.uint import UIntT
from py_hcl.utils import auto_repr


class ConnLoc(Enum):
    UNKNOWN = 0
    LF = 1
    RT = 2
    BOTH = 3


@auto_repr
class Connect(object):
    def __init__(self, left, right):
        self.left = left
        self.right = right


connector = op_register('<<=')


@connector(UIntT, UIntT)
def _(left, right):
    check_connect_dir(left, right)

    if left.hcl_type.width < right.hcl_type.width:
        msg = 'connect(): connecting {} to {} will truncate the bits'.format(
            right.hcl_type, left.hcl_type)
        logging.warning(msg)
        right = right[left.hcl_type.width - 1:0]

    assert left.hcl_type.width >= right.hcl_type.width
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

    StatementTrapper.track(Connect(left, right))
    return left


@connector(UIntT, SIntT)
def _(left, right):
    msg = 'connect(): connecting SInt to UInt, an auto-conversion will occur'
    logging.warning(msg)
    return op_apply('<<=')(left, right.to_uint())


@connector(SIntT, UIntT)
def _(left, right):
    msg = 'connect(): connecting UInt to SInt, an auto-conversion will occur'
    logging.warning(msg)
    return op_apply('<<=')(left, right.to_sint())


@connector(object, object)
def _(_0, _1):
    raise StatementError.connect_type_error(_0, _1)


def check_connect_dir(left, right):
    assert left.conn_loc in (ConnLoc.LF, ConnLoc.BOTH)
    assert right.conn_loc in (ConnLoc.RT, ConnLoc.BOTH)
