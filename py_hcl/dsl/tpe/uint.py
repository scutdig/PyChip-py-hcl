from py_hcl.dsl.expr.u_literal import ULiteral
from py_hcl.dsl.tpe.hcl_type import HclType


class UIntT(HclType):
    def __init__(self, width):
        self.width = width

    def __call__(self, value):
        return ULiteral(value)  # TODO: check width


def U(value):
    return ULiteral(value)


U.w = UIntT
Bool = U.w(1)
