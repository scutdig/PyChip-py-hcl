from py_hcl.core.type import HclType
from py_hcl.core.expr.uint_lit import ULiteral


class UIntT(HclType):
    def __init__(self, width):
        self.width = width

    def __call__(self, value):
        return ULiteral(value)  # TODO: check width
