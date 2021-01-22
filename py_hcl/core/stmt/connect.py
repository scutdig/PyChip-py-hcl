"""
Implement connection between two PyHCL expressions.

Examples
--------

>>> from py_hcl import *

Connect literal to output:

>>> class _(Module):
...     io = IO(o=Output(U.w(5)))
...     io.o <<= U(10)


Connect input to output:

>>> class _(Module):
...     io = IO(i=Input(U.w(8)), o=Output(U.w(5)))
...     io.o <<= io.i


Connect wire to output and connect input to wire:

>>> class _(Module):
...     io = IO(i=Input(U.w(8)), o=Output(U.w(5)))
...     w = Wire(U.w(6))
...     io.o <<= w
...     w <<= io.i


Connection with wrong direction

>>> class _(Module):
...     io = IO(i=Input(U.w(8)))
...     lit = U(8)
...     lit <<= io.i
Traceback (most recent call last):
...
py_hcl.core.stmt.error.StatementError: Connection statement with unexpected
direction.
"""

import logging
from enum import Enum

from py_hcl.core.hcl_ops import op_register, op_apply
from py_hcl.core.stmt.error import StatementError
from py_hcl.core.stmt_factory.trapper import StatementTrapper
from py_hcl.core.type import HclType
from py_hcl.core.type.bundle import BundleT, BundleDirection
from py_hcl.core.type.sint import SIntT
from py_hcl.core.type.uint import UIntT
from py_hcl.core.type.vector import VectorT
from py_hcl.utils.serialization import json_serialize


class VariableType(Enum):
    UNKNOWN = 0
    WriteOnly = 1
    ReadOnly = 2
    ReadWrite = 3


@json_serialize
class Connect(object):
    def __init__(self, left, right):
        self.stmt_type = 'connect'
        self.left_expr_id = left.id
        self.right_expr_id = right.id


connector = op_register('<<=')


def check_connect_direction(f):
    def _(left: HclType, right: HclType):
        if left.variable_type not in (VariableType.WriteOnly,
                                      VariableType.ReadWrite):
            direction = left.variable_type
            raise StatementError.connect_direction_error(
                f'The lhs of connection statement can not be a {direction}')
        if right.variable_type not in (VariableType.ReadOnly,
                                       VariableType.ReadWrite):
            direction = right.variable_type
            raise StatementError.connect_direction_error(
                f'The rhs of connection statement can not be a {direction}')

        return f(left, right)

    return _


@connector(UIntT, UIntT)
@check_connect_direction
def _(left, right):
    if left.hcl_type.width < right.hcl_type.width:
        logging.warning(
            f'connect(): connecting {right.hcl_type} to {left.hcl_type} '
            f'will truncate the bits')
        right = right[left.hcl_type.width - 1:0]

    if left.hcl_type.width > right.hcl_type.width:
        right = op_apply('extend')(right, left.hcl_type.width)

    assert left.hcl_type.width == right.hcl_type.width
    StatementTrapper.track(Connect(left, right))
    return left


@connector(SIntT, SIntT)
@check_connect_direction
def _(left, right):
    if left.hcl_type.width < right.hcl_type.width:
        logging.warning(
            f'connect(): connecting {right.hcl_type} to {left.hcl_type} '
            f'will truncate the bits')
        right = right[left.hcl_type.width - 1:0].to_sint()

    if left.hcl_type.width > right.hcl_type.width:
        right = op_apply('extend')(right, left.hcl_type.width)

    assert left.hcl_type.width == right.hcl_type.width
    StatementTrapper.track(Connect(left, right))
    return left


@connector(UIntT, SIntT)
@check_connect_direction
def _(left, right):
    logging.warning(
        'connect(): connecting SInt to UInt will cause auto-conversion')

    if left.hcl_type.width < right.hcl_type.width:
        logging.warning(
            f'connect(): connect {right.hcl_type} to {left.hcl_type} '
            f'will truncate the bits')
        return op_apply('<<=')(left, right[left.hcl_type.width - 1:0])

    return op_apply('<<=')(left, right.to_uint())


@connector(SIntT, UIntT)
@check_connect_direction
def _(left, right):
    logging.warning(
        'connect(): connecting UInt to SInt will cause auto-conversion')

    if left.hcl_type.width < right.hcl_type.width:
        logging.warning(
            f'connect(): connecting {right.hcl_type} to {left.hcl_type} '
            f'will truncate the bits')
        right = right[left.hcl_type.width - 1:0]

    return op_apply('<<=')(left, right.to_sint())


@connector(BundleT, BundleT)
@check_connect_direction
def _(left, right):
    # TODO: Accurate Error Message
    dir_and_types = right.hcl_type.fields
    keys = dir_and_types.keys()
    assert keys == left.hcl_type.fields.keys()

    for k in keys:
        lf = op_apply('.')(left, k)
        rt = op_apply('.')(right, k)
        if dir_and_types[k]['dir'] == BundleDirection.SOURCE:
            op_apply('<<=')(lf, rt)
        else:
            op_apply('<<=')(rt, lf)

    return left


@connector(VectorT, VectorT)
@check_connect_direction
def _(left, right):
    # TODO: Accurate Error Message
    assert left.hcl_type.size == right.hcl_type.size

    for i in range(left.hcl_type.size):
        op_apply('<<=')(left[i], right[i])

    return left


@connector(HclType, HclType)
def _(_0, _1):
    raise StatementError.connect_type_error(_0, _1)
