from .expr.literal import UIntLiteral, SIntLiteral
from .expr.reference import Reference
from .type import SIntType, UIntType, VectorType, BundleType
from .type.field import Field
from .type.width import Width


def sw(width):
    return SIntType(Width(width))


def uw(width):
    return UIntType(Width(width))


def w(width):
    return Width(width)


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
