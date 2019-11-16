from ..expr.reference import Reference
from .literal import LiteralTypeChecker
from .mux import MuxTypeChecker
from .prim_ops import OpTypeChecker
from .accessor import AccessorTypeChecker

final_map = {
    **OpTypeChecker.op_checker_map,
    **MuxTypeChecker.mux_checker_map,
    **AccessorTypeChecker.accessor_checker_map,
    **LiteralTypeChecker.literal_checker_map,

    # simple expresion
    Reference: lambda _: True
}


def check(obj):
    try:
        return final_map[type(obj)](obj)
    except (KeyError, NotImplementedError):
        return False


def check_all(*obj):
    return all(check(o) for o in obj)
