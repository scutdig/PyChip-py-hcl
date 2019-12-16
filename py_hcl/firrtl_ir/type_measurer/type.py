from multipledispatch import dispatch

from ..type import UnknownType, UIntType, SIntType, \
    ClockType, BundleType, VectorType

measurer = dispatch


@measurer(UnknownType, UnknownType)
def equal(_0: UnknownType, _1: UnknownType):
    return True


@measurer(UIntType, UIntType)
def equal(t1: UIntType, t2: UIntType):
    return equal(t1.width, t2.width)


@measurer(SIntType, SIntType)
def equal(t1: SIntType, t2: SIntType):
    return equal(t1.width, t2.width)


@measurer(ClockType, ClockType)
def equal(_0: ClockType, _1: ClockType):
    return True


@measurer(BundleType, BundleType)
def equal(t1: BundleType, t2: BundleType):
    if len(t1.fields) != len(t2.fields):
        return False
    for (a, b) in zip(t1.fields, t2.fields):
        if not equal(a, b):
            return False
    return True


@measurer(VectorType, VectorType)
def equal(t1: VectorType, t2: VectorType):
    if t1.size != t2.size:
        return False
    if not equal(t1.elem_type, t2.elem_type):
        return False
    return True
