from .stmt.definition import DefinitionTypeChecker
from .stmt.block import BlockTypeChecker
from .stmt.conditionally import ConditionallyTypeChecker
from ..stmt import Statement
from ..expr import Expression
from .stmt.connect import ConnectTypeChecker
from ..stmt.empty import EmptyStmt
from ..expr.reference import Reference
from .expr.literal import LiteralTypeChecker
from .expr.mux import MuxTypeChecker
from .expr.prim_ops import OpTypeChecker
from .expr.accessor import AccessorTypeChecker


def true(_):
    return True


final_map = {
    **OpTypeChecker.op_checker_map,
    **MuxTypeChecker.mux_checker_map,
    **AccessorTypeChecker.accessor_checker_map,
    **LiteralTypeChecker.literal_checker_map,

    # simple expresion
    Reference: true,

    **ConnectTypeChecker.connect_checker_map,
    **ConditionallyTypeChecker.conditionally_checker_map,
    **BlockTypeChecker.block_checker_map,
    **DefinitionTypeChecker.definition_checker_map,

    # simple statement
    EmptyStmt: true,
}


def check(obj):
    try:
        return final_map[type(obj)](obj)
    except (KeyError, NotImplementedError):
        return False


def check_all_expr(*obj):
    return all(isinstance(o, Expression) and check(o) for o in obj)


def check_all_stmt(*obj):
    return all(isinstance(o, Statement) and check(o) for o in obj)
