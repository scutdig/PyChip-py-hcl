from ..tpe import UnknownType, UIntType, SIntType, \
    ClockType, BundleType, VectorType


class TypeMeasurer(object):
    measurer_map = {}

    @staticmethod
    def equal(x, y):
        try:
            return TypeMeasurer.measurer_map[(type(x), type(y))](x, y)
        except KeyError:
            raise NotImplementedError((type(x), type(y)))


def measurer(clz, cls):
    def f(func):
        TypeMeasurer.measurer_map[(clz, cls)] = func
        return func

    return f


@measurer(UnknownType, UnknownType)
def _(t1, t2):
    return True


@measurer(UIntType, UIntType)
def _(t1, t2):
    from .width import WidthMeasurer
    return WidthMeasurer.equal(t1.width, t2.width)


@measurer(SIntType, SIntType)
def _(t1, t2):
    from .width import WidthMeasurer
    return WidthMeasurer.equal(t1.width, t2.width)


@measurer(ClockType, ClockType)
def _(t1, t2):
    return True


@measurer(BundleType, BundleType)
def _(t1, t2):
    if len(t1.fields) != len(t2.fields):
        return False
    from .field import FieldMeasurer
    for (a, b) in zip(t1.fields, t2.fields):
        if not FieldMeasurer.equal(a, b):
            return False
    return True


@measurer(VectorType, VectorType)
def _(t1, t2):
    if t1.size != t2.size:
        return False
    if not TypeMeasurer.equal(t1.elem_type, t2.elem_type):
        return False
    return True
