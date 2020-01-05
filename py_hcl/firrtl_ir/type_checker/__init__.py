from multipledispatch import dispatch
import logging

from .stmt.definition import check
from .stmt.block import check
from .stmt.conditionally import check
from ..stmt import Statement
from ..expr import Expression
from .stmt.connect import check
from ..stmt.empty import EmptyStmt
from ..expr.reference import Reference
from .expr.literal import check
from .expr.mux import check
from .expr.prim_ops import check
from .expr.accessor import check

checker = dispatch


@checker(EmptyStmt)
def check(_: EmptyStmt):
    return True


@checker(Reference)
def check(_: Reference):
    return True


@checker(object)
def check(_: object):
    logging.error("unsupported type: " + _.__class__.__name__)
    return False


def check_all_expr(*obj):
    return all(isinstance(o, Expression) and check(o) for o in obj)


def check_all_stmt(*obj):
    return all(isinstance(o, Statement) and check(o) for o in obj)
