from py_hcl.core.type.uint import UIntT
from py_hcl.core.expr.uint_lit import ULiteral


def U(value):
    return ULiteral(value)


def uw(width):
    return UIntT(width)


U.w = uw
Bool = U.w(1)
