from py_hcl.core.expr.lit_uint import ULiteral
from py_hcl.core.type.uint import UIntT


class _(object):
    def __call__(self, value: int) -> ULiteral:
        return ULiteral(value)

    @staticmethod
    def w(width: int) -> UIntT:
        return UIntT(width)


U = _()
Bool = U.w(1)
