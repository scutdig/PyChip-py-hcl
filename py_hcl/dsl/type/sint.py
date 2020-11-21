from py_hcl.core.expr.lit_sint import SLiteral
from py_hcl.core.type.sint import SIntT


class _(object):
    def __call__(self, value: int) -> SLiteral:
        return SLiteral(value)

    @staticmethod
    def w(width: int) -> SIntT:
        return SIntT(width)


S = _()
