from py_hcl.firrtl_ir.type.field import Field


class FieldMeasurer(object):
    measurer_map = {}

    @staticmethod
    def equal(x, y):
        try:
            return FieldMeasurer.measurer_map[(type(x), type(y))](x, y)
        except KeyError:
            raise NotImplementedError((type(x), type(y)))


def measurer(clz, cls):
    def f(func):
        FieldMeasurer.measurer_map[(clz, cls)] = func
        return func

    return f


@measurer(Field, Field)
def _(f1, f2):
    if f1.name != f2.name:
        return False
    if f1.is_flipped != f2.is_flipped:
        return False

    from .type import TypeMeasurer
    return TypeMeasurer.equal(f1.tpe, f2.tpe)
