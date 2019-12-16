from py_hcl.core.type.uint import UIntT
from py_hcl.core.expr.uint_lit import ULiteral


class U(object):
    def __call__(self, value: int):
        return ULiteral(value)

    @staticmethod
    def w(width: int):
        return UIntT(width)


U = U()
Bool = U.w(1)
