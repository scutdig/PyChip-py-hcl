from .field import Field
from .reference import Reference
from .literal import UIntLiteral, SIntLiteral
from .tpe import SIntType, UIntType, VectorType, BundleType
from .width import IntWidth


def sw(width):
    return SIntType(IntWidth(width))


def uw(width):
    return UIntType(IntWidth(width))


def w(width):
    return IntWidth(width)


def u(value, width):
    return UIntLiteral(value, width)


def s(value, width):
    return SIntLiteral(value, width)


def n(name, tpe):
    return Reference(name, tpe)


def vec(tpe, size):
    return VectorType(tpe, size)


def bdl(**field):
    fields = [Field(k, field[k][0], field[k][1]) for k in field]
    return BundleType(fields)
